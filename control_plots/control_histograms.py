import ROOT, sys

from tree_inputs import input_files
from trlib import initialize_tree, var_list, pass_trigger_selection, pass_lepton_selection, pass_jet_selection, bjet_presel, event_count
from histlib import hist_variables, initialize_histograms, fill_1D_histograms, fill_lepton_histograms, fill_jet_histograms, write_histograms_to_file

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='DL_or_SL',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
parser.add_argument('--testRun', dest='is_test_run', action="store_true", default=False, required=False)
parser.add_argument('--sel', dest="sel", choices=["pre","pre_2b"], default=False, required=False)
args = parser.parse_args()
mode = args.DL_or_SL

if args.DL_or_SL == "DL":
    print "Starting dilepton analysis"

if args.DL_or_SL == "SL":
    print "Starting single lepton analysis"

indir = "test_trees/trees_2014_02_09_0-0-1_rec_reg/"

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
    cut_flow[proc] = ROOT.TH1F("cut_flow_" + proc, "cut_flow_" + proc, 15, 0 , 15 )

    if proc == "TTJets": # initialize extra histograms for ttJets, separating by gen level decay
        isTTjets = True
        for sub_proc in ["ttbb", "ttb", "ttjj"]:
            hists[sub_proc] = initialize_histograms(sub_proc, hist_variables)
            cut_flow[sub_proc] = ROOT.TH1F("cut_flow_" + sub_proc, "cut_flow_" + sub_proc, 15, 0, 15)

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
            weight = ev_weight*pu_weight*19/12 #*tr_weight

        #-------------select events---------------
        
        event_count(0, cut_flow, proc, weight, vd) # cut-flow: all evts

        if proc[-7:] == "Mu_data" and not( pass_trigger_selection(vd, mode, "mu") ): continue
        if proc[-7:] == "El_data" and not( pass_trigger_selection(vd, mode, "el") ): continue

        event_count(1, cut_flow, proc, weight, vd) # cut_flow: apply trigger for data

        sel_lep = pass_lepton_selection(vd, mode) # count the number of good electrons and apply preselection

        if len(sel_lep) == 0: continue 
        event_count(2, cut_flow, proc, weight, vd) # cut_flow: require one lepton


        if vd["numJets"][0] >= 6 and vd["numBTagM"][0] == 2:
            event_count(3, cut_flow, proc, weight, vd) # cut_flow: Category 1 ttH
            
            fill_1D_histograms( vd, hists, proc, weight, mode, isTTjets )
            fill_lepton_histograms( vd, hists, proc, weight, mode, sel_lep, isTTjets)
            fill_jet_histograms(vd, hists, proc, weight, mode, isTTjets = isTTjets)                         


        if vd["numJets"][0] == 4  and vd["numBTagM"][0] == 3:
            event_count(4, cut_flow, proc,weight, vd)

        if vd["numJets"][0] == 5 and vd["numBTagM"][0] == 3:
            event_count(5, cut_flow, proc,weight, vd)

        if vd["numJets"][0] >=6 and vd["numBTagM"][0] == 3:
            event_count(6, cut_flow, proc,weight, vd)

        if vd["numJets"][0] == 4 and vd["numBTagM"][0] ==4:
            event_count(7, cut_flow, proc,weight, vd)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=4:
            event_count(8, cut_flow, proc,weight, vd)

        if vd["numJets"][0] >=6 and vd["numBTagM"][0] >=4:
            event_count(9, cut_flow, proc,weight, vd)

        #------lorenzo categories-----------

        if vd["numJets"][0] ==6 and vd["numBTagM"][0] >=4: # cat 1, 2
            event_count(10, cut_flow, proc,weight, vd)

        if vd["numJets"][0] >= 7 and vd["numBTagM"][0] >= 4: # cat 5
            event_count(11, cut_flow, proc, weight, vd)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >= 4: # cat 3, 4
            event_count(12, cut_flow, proc,weight, vd)
            
        #------according to vtypes--------
        if vd["flag_type0"][0] >= -10:
            event_count(13, cut_flow, proc, weight, vd)
        if vd["flag_type1"][0] >= -10:
            event_count(14, cut_flow, proc, weight, vd)
        if vd["flag_type2"][0] >= -10:
            event_count(15, cut_flow, proc, weight, vd)
        if vd["flag_type3"][0] >= -10:
            event_count(16, cut_flow, proc, weight, vd)
#        if vd["flag_type4"][0] >= 0:
#            event_count(14, cut_flow, proc, weight, vd)

    print "--------- CUT FLOW ------------- "
    print "Nr tot = "+  str(cut_flow[proc].GetBinContent(1))
    print "Nr trig sel = " + str(cut_flow[proc].GetBinContent(2))
    print "Nr lep sel = " + str(cut_flow[proc].GetBinContent(3))
    print ">=6 jets + 2 tags: " + str(cut_flow[proc].GetBinContent(4))
    print "4 jets 3 tags: "  + str(cut_flow[proc].GetBinContent(5))
    print "5 jets 3 tags: "  + str(cut_flow[proc].GetBinContent(6))
    print ">=6 jets 3 tags: "  + str(cut_flow[proc].GetBinContent(7))
    print " 4 jets 4 tags: " + str(cut_flow[proc].GetBinContent(8))
    print " 5 jets >=4 tags: " + str(cut_flow[proc].GetBinContent(9))
    print ">= 6 jets >= 4 tags " + str(cut_flow[proc].GetBinContent(10))
    print"---------Lorenzo categories---------------"
    print "cat1, cat2: " + str(cut_flow[proc].GetBinContent(11))
    print "cat5 : " + str(cut_flow[proc].GetBinContent(12))
    print "cat 3, cat 4: " + str(cut_flow[proc].GetBinContent(13))
#    print "type 3: " + str(cut_flow[proc].GetBinContent(14))
#    print "type 4: " + str(cut_flow[proc].GetBinContent(15))

    
#    print ">6 jets > 4 tag = " + str(cut_flow[proc].GetBinContent(6))
#    print "vtype0 or vtype1 " + str(cut_flow[proc].GetBinContent(7))

#    print "5 jets 4 tag = " + str(cut_flow[proc].GetBinContent(8))

sel = "presel_2b_"
outdir = "./histograms/"
outfilename = outdir + "histograms_" + sel + mode + ".root"
print "Write output to file: " + outfilename 


write_histograms_to_file(outfilename, hists, cut_flow)
#for proc in cut_flow:
#    cut_flow[proc].Write()
        
        
        


        
        
