import ROOT, sys

from tree_inputs import input_files
from trlib import initialize_tree, var_list, pass_trigger_selection, pass_lepton_selection, pass_jet_selection, bjet_presel, event_count
from histlib import hist_variables, initialize_histograms, fill_1D_histograms, fill_lepton_histograms, fill_jet_histograms, fill_single_histogram, write_histograms_to_file

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='DL_or_SL',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
parser.add_argument('--testRun', dest='is_test_run', action="store_true", default=False, required=False)
parser.add_argument('--sel', dest="sel", choices=["pre","pre_2b"], default=False, required=False)
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
parser.add_argument('--notopw', dest="notopw", action="store_true", default=False, required=False) # dont apply top pt reweight
                   
args = parser.parse_args()
mode = args.DL_or_SL
notopw=args.notopw

if args.DL_or_SL == "DL":
    print "Starting dilepton analysis"

if args.DL_or_SL == "SL":
    print "Starting single lepton analysis"

##indir = "test_trees/trees_2014_02_09_0-0-1_rec_std/"
#indir = "test_trees/trees_2014_02_15_0-0-1_rec_std/"
indir = "test_trees/trees_2014_02_24_0-0-1_rec_std/"
usetrig = not args.notrig

Lumi = 19.04

pars = ROOT.TH1F("pars", "pars", 10, 0, 10)
pars.SetBinContent(1, Lumi)
pars.GetXaxis().SetBinLabel(1, "Lumi")

f_all = {}
t_all = {}
for sample in input_files:
    if mode == "DL" and (sample[:6] == "single"): continue
    if mode == "SL" and (sample[:2] == "di"): continue
    print "Opening sample: " + sample
    f_all[sample] = ROOT.TFile(indir + input_files[sample])
    t_all[sample] = f_all[sample].Get("tree")

            

report_every = 100000
if args.is_test_run:
    max_event = 10000
else:
    max_event = -1

hists = {} #histograms for each sample and variable
cut_flow = {}
btag_LR_5j = {}
btag_LR_6j = {}
btag_LR_7j = {}
for proc, tree in t_all.iteritems():
    print "Processing: " + proc + " tree with " + str(tree.GetEntries()) + "events"

    isTTjets = False
    hists[proc] = initialize_histograms(proc, hist_variables) # dictionary of initialized histograms for each sample
    cut_flow[proc] = ROOT.TH1F("cut_flow_" + proc, "cut_flow_" + proc, 25, 0 , 25 )
    cut_flow[proc].Sumw2()

    btag_LR_5j[proc] = ROOT.TH1F("btag_lr_5j_" + proc, "btag_lr_5j_" + proc, 50, 0, 1)
    btag_LR_5j[proc].Sumw2()
    btag_LR_7j[proc] = ROOT.TH1F("btag_lr_7j_" + proc, "btag_lr_7j_" + proc, 50, 0, 1)
    btag_LR_7j[proc].Sumw2()
    btag_LR_6j[proc] = ROOT.TH1F("btag_lr_6j_" + proc, "btag_lr_6j_" + proc, 50, 0, 1)
    btag_LR_6j[proc].Sumw2()
               

    if proc == "TTJets": # initialize extra histograms for ttJets, separating by gen level decay
        isTTjets = True
        for sub_proc in ["ttbb", "ttb", "ttjj"]:
            hists[sub_proc] = initialize_histograms(sub_proc, hist_variables)
            cut_flow[sub_proc] = ROOT.TH1F("cut_flow_" + sub_proc, "cut_flow_" + sub_proc, 25, 0, 25)
            cut_flow[sub_proc].Sumw2()
            
            btag_LR_5j[sub_proc] = ROOT.TH1F("btag_lr_5j_" + sub_proc, "btag_lr_5j_" + sub_proc, 50, 0, 1)
            btag_LR_6j[sub_proc] = ROOT.TH1F("btag_lr_6j_" + sub_proc, "btag_lr_6j_" + sub_proc, 50, 0, 1)
            btag_LR_7j[sub_proc] = ROOT.TH1F("btag_lr_7j_" + sub_proc, "btag_lr_7j_" + sub_proc, 50, 0, 1)
            
    
    vd = initialize_tree(tree, var_list) # dictionary of variables

    for i in range( tree.GetEntries() ):
        if i % report_every == 0: 
            print "Event nr: " + str(i)
        if i == max_event and not i == -1: break            

        tree.LoadTree(i)
        tree.GetEntry(i)
        ev_weight = vd["weight"][0]
        tr_weight = vd["trigger"][0]
        pu_weight = vd["PUweight"][0]
        toppt_weight = vd["weightTopPt"][0]

        if proc[-4:] == "data":
            weight = 1
        else:
            weight = ev_weight*pu_weight*Lumi/12
            if not notopw:
                weight = weight*toppt_weight
            if usetrig:
                weight = weight*tr_weight

            
        #-------------select events---------------

        event_count(0, "all", cut_flow, proc, weight, vd) # cut-flow: all evts

        if proc[-7:] == "Mu_data" and not( pass_trigger_selection(vd, mode, "mu") ): continue #FIXME - currently trig and lep sel together to avoid triggering electron and selecting muon
        if proc[-7:] == "El_data" and not( pass_trigger_selection(vd, mode, "el") ): continue

        event_count(1, "trig", cut_flow, proc, weight, vd) # cut_flow: apply trigger for data
        sel_lep = pass_lepton_selection(vd, mode) # count the number of good leptons and apply preselection
        if not ( len(sel_lep) ): continue

#        if not (proc[-7:] == "Mu_data" and vd["Vtype"][0] == 3): continue
#        if not (proc[-7:] == "El_data" and vd["Vtype"][0] == 2): continue


#        if not (vd["Vtype"][0] == 3 or vd["Vtype"][0] == 2): continue
        event_count(2, "SelLep", cut_flow, proc, weight, vd) # cut_flow: require one lepton

        sel_jet = pass_jet_selection(vd, mode, jet40=True)
        if not( len(sel_jet) ):continue
        if vd["numJets"][0] >= 6 and vd["numBTagM"][0] >= 2:
            fill_1D_histograms( vd, hists, proc, weight, mode, isTTjets )
            fill_lepton_histograms( vd, hists, proc, weight, mode, sel_lep, isTTjets)
            fill_jet_histograms(vd, hists, proc, weight, mode, isTTjets = isTTjets)

        if vd["numJets"][0] >= 7: 
            fill_single_histogram(vd, btag_LR_7j, proc, vd["btag_LR"][0], weight, isTTjets = isTTjets)
                                  
        #    btag_LR_7j[proc].Fill(vd["btag_LR"][0])
        #    if isTTjets:
        #        if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
        #            btag_LR_7j["ttbb"].Fill(vd["btag_LR"][0], weight)
        #        elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
        #            btag_LR_7j["ttb"].Fill(vd["btag_LR"][0], weight)
        #        elif vd["nSimBs"][0] == 2:
        #            btag_LR_7j["ttjj"].Fill(vd["btag_LR"][0], weight)

                                    
            
 #       if vd["numJets"][0] == 6: # and vd["numBTagM"][0] >= 2:
 #           btag_LR_6j[proc].Fill(vd["btag_LR"][0])
 #           if isTTjets:
 #               if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
 #                   btag_LR_6j["ttbb"].Fill(vd["btag_LR"][0], weight)
 #               elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
 #                   btag_LR_6j["ttb"].Fill(vd["btag_LR"][0], weight)
 #               elif vd["nSimBs"][0] == 2:
 #                   btag_LR_6j["ttjj"].Fill(vd["btag_LR"][0], weight)

 #       if vd["numJets"][0] == 5: # and vd["numBTagM"][0] >= 2:
 #           btag_LR_5j[proc].Fill(vd["btag_LR"][0])
 #           if isTTjets:
 #               if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
 #                   btag_LR_5j["ttbb"].Fill(vd["btag_LR"][0], weight)
 #               elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
 #                   btag_LR_5j["ttb"].Fill(vd["btag_LR"][0], weight)
 #               elif vd["nSimBs"][0] == 2:
 #                   btag_LR_5j["ttjj"].Fill(vd["btag_LR"][0], weight)

        if vd["numJets"][0] >= 6 and vd["numBTagM"][0] == 2:
            event_count(3, "g6j2t", cut_flow, proc, weight, vd ) # cut_flow, preselection


        if vd["numJets"][0] == 4  and vd["numBTagM"][0] == 3:
            event_count(4, "4j3t",  cut_flow, proc,weight, vd)

        if vd["numJets"][0] == 5 and vd["numBTagM"][0] == 3:
            event_count(5, "5j3t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] >=6 and vd["numBTagM"][0] == 3:
            event_count(6, "g6j3t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] == 4 and vd["numBTagM"][0] ==4:
            event_count(7, "4j4t", cut_flow, proc,weight, vd)

        if vd["numBTagM"][0] ==4:
            event_count(8, "g4j4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=4:
            event_count(9, "5jg4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] >=6 and vd["numBTagM"][0] >=4:
            event_count(10, "g6jg4t", cut_flow, proc,weight, vd)

        #------lorenzo categories-----------

        if vd["numJets"][0] ==6 and vd["numBTagM"][0] >=4: # cat 1, 2
            event_count(24, "L6jg4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] >= 7 and vd["numBTagM"][0] >= 4 and vd["numBTagM"][0]: # cat 5
            event_count(11, "Lg7jg4t", cut_flow, proc, weight, vd)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >= 4: # cat 3, 4
            event_count(12, "L5jg4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] ==6 and vd["numBTagM"][0] ==4: # cat 1, 2
            event_count(13, "L6j4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] >= 7 and vd["numBTagM"][0] == 4: # cat 5
            event_count(14, "Lg7j4t", cut_flow, proc, weight, vd)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] == 4: # cat 3, 4
            event_count(15, "L5j4t", cut_flow, proc,weight, vd)
            
        if vd["numBTagM"][0] >=4:
            event_count(16, "g4t", cut_flow, proc,weight, vd)
            
        if vd["numBTagM"][0] ==3 and vd["numBTagL"][0]==4:
            event_count(17, "3t1t", cut_flow, proc,weight, vd)
            
        #------according to event type --------
        if vd["type"][0] == 0:
            event_count(18, "cat1", cut_flow, proc, weight, vd)
        if vd["type"][0] == 1:
            event_count(19, "cat2", cut_flow, proc, weight, vd)
        if vd["type"][0] == 2:
            event_count(20, "cat3_4", cut_flow, proc, weight, vd)
        if vd["type"][0] == 3:
            event_count(21, "cat5", cut_flow, proc, weight,vd)
        if vd["type"][0] == 6:
            event_count(22, "cat6", cut_flow, proc, weight,vd)
        if vd["type"][0] == 7:
            event_count(23, "cat7", cut_flow, proc, weight,vd)

    print "--------- CUT FLOW ------------- "
    print "Nr tot = "+  str(cut_flow[proc].GetBinContent(1))
    print "Nr trig sel = " + str(cut_flow[proc].GetBinContent(2))
    print "Nr lep sel = " + str(cut_flow[proc].GetBinContent(3))

    if mode == "SL":
        print ">=6 jets + 2 tags: " + str(cut_flow[proc].GetBinContent(4))

        print "6 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L6jg4t")) )
        print "5 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L5jg4t")) )
        print ">=6 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("Lg7jg4t")) )
        
        print "type 1: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat1")) )
        print "type 2: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat2")) )
        print "type 3/4: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat3_4")) )
        print "type 5: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat5")) )

    if mode == "DL":
        print "g4j4t: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("g4j4t")) )
        print "3M1L: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("3t1t")) )
        print "type 6: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat6")) )
        print "type 7: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat7")) )

sel = "presel_2b_"
outdir = "./histograms/"

outfilename = outdir + "histograms_" + sel + mode
if not usetrig:
    outfilename = outfilename + "_notrig" 
if notopw:
    outfilename = outfilename + "_notopw"

outfilename = outfilename + ".root"
    
print "Write output to file: " + outfilename 
write_histograms_to_file(outfilename, hists, [cut_flow], [pars])

        
        


        
        
