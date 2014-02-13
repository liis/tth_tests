import ROOT, sys

from tree_inputs import input_files
from trlib import initialize_tree, var_list, pass_trigger_selection, pass_lepton_selection, pass_jet_selection, bjet_presel, event_count
from histlib import hist_variables, initialize_histograms, fill_1D_histograms, fill_lepton_histograms, fill_jet_histograms, write_histograms_to_file

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='DL_or_SL',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
parser.add_argument('--testRun', dest='is_test_run', action="store_true", default=False, required=False)
parser.add_argument('--sel', dest="sel", choices=["pre","pre_2b"], default=False, required=False)
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
                   
args = parser.parse_args()
mode = args.DL_or_SL

if args.DL_or_SL == "DL":
    print "Starting dilepton analysis"

if args.DL_or_SL == "SL":
    print "Starting single lepton analysis"

indir = "test_trees/trees_2014_02_09_0-0-1_rec_std/"

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
for proc, tree in t_all.iteritems():
    print "Processing: " + proc + " tree with " + str(tree.GetEntries()) + "events"

    isTTjets = False
    hists[proc] = initialize_histograms(proc, hist_variables) # dictionary of initialized histograms for each sample
    cut_flow[proc] = ROOT.TH1F("cut_flow_" + proc, "cut_flow_" + proc, 25, 0 , 25 )
    cut_flow[proc].Sumw2()

    if proc == "TTJets": # initialize extra histograms for ttJets, separating by gen level decay
        isTTjets = True
        for sub_proc in ["ttbb", "ttb", "ttjj"]:
            hists[sub_proc] = initialize_histograms(sub_proc, hist_variables)
            cut_flow[sub_proc] = ROOT.TH1F("cut_flow_" + sub_proc, "cut_flow_" + sub_proc, 25, 0, 25)
            cut_flow[sub_proc].Sumw2()

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

        if proc[-4:] == "data":
            weight = 1
        else:
            weight = ev_weight*pu_weight*Lumi/12
            if usetrig:
                weight = weight*tr_weight

            
        #-------------select events---------------

        event_count(0, "all", cut_flow, proc, weight, vd) # cut-flow: all evts

        if proc[-7:] == "Mu_data" and not( pass_trigger_selection(vd, mode, "mu") ): continue
        if proc[-7:] == "El_data" and not( pass_trigger_selection(vd, mode, "el") ): continue

        event_count(1, "trig", cut_flow, proc, weight, vd) # cut_flow: apply trigger for data

        sel_lep = pass_lepton_selection(vd, mode) # count the number of good electrons and apply preselection

        if len(sel_lep) == 0: continue

        event_count(2, "SelLep", cut_flow, proc, weight, vd) # cut_flow: require one lepton


        if vd["numJets"][0] >= 6 and vd["numBTagM"][0] == 2:
            event_count(3, "g6j2t", cut_flow, proc, weight, vd ) # cut_flow: Category 1 ttH

            fill_1D_histograms( vd, hists, proc, weight, mode, isTTjets )
            fill_lepton_histograms( vd, hists, proc, weight, mode, sel_lep, isTTjets)
            fill_jet_histograms(vd, hists, proc, weight, mode, isTTjets = isTTjets)                         


        if vd["numJets"][0] == 4  and vd["numBTagM"][0] == 3:
            event_count(4, "4j3t",  cut_flow, proc,weight, vd)

        if vd["numJets"][0] == 5 and vd["numBTagM"][0] == 3:
            event_count(5, "5j3t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] >=6 and vd["numBTagM"][0] == 3:
            event_count(6, "g6j3t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] == 4 and vd["numBTagM"][0] ==4:
            event_count(7, "4j4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=4:
            event_count(8, "5jg4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] >=6 and vd["numBTagM"][0] >=4:
            event_count(9, "g6jg4t", cut_flow, proc,weight, vd)

        #------lorenzo categories-----------

        if vd["numJets"][0] ==6 and vd["numBTagM"][0] >=4: # cat 1, 2
            event_count(10, "L6jg4t", cut_flow, proc,weight, vd)

        if vd["numJets"][0] >= 7 and vd["numBTagM"][0] >= 4: # cat 5
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
            
        if vd["numBTagM"][0] ==3 and vd["numBTagL"][0]==1:
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
        if vd["type"][0] == 5:
            event_count(22, "cat6", cut_flow, proc, weight,vd)
        if vd["type"][0] == 6:
            event_count(23, "cat7", cut_flow, proc, weight,vd)

    print "--------- CUT FLOW ------------- "
    print "Nr tot = "+  str(cut_flow[proc].GetBinContent(1))
    print "Nr trig sel = " + str(cut_flow[proc].GetBinContent(2))
    print "Nr lep sel = " + str(cut_flow[proc].GetBinContent(3))
    print ">=6 jets + 2 tags: " + str(cut_flow[proc].GetBinContent(4))
    print ">= 6 jets >= 4 tags " + str(cut_flow[proc].GetBinContent(9))
    print " 4 jets 4 tags: " + str(cut_flow[proc].GetBinContent(7))
    print "----------DL relevant---------------------"
    print " >= 4 tags: " + str(cut_flow[proc].GetBinContent(16))
    print " >= 3 tags: " + str(cut_flow[proc].GetBinContent(17) )


sel = "presel_2b_"
outdir = "./histograms/"

outfilename = outdir + "histograms_" + sel + mode + ".root"
if not usetrig:
    outfilename = outfilename.rsplit(".root")[0] + "_notrig.root" 
    
print "Write output to file: " + outfilename 

write_histograms_to_file(outfilename, hists, cut_flow, [pars])
        
        
        


        
        
