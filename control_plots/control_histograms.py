import ROOT, sys

from tree_inputs import input_files
from trlib import initialize_tree, var_list, pass_trigger_selection, pass_lepton_selection, pass_jet_selection
from histlib import hist_variables, initialize_histograms, write_histograms_to_file

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='DL_or_SL',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
parser.add_argument('--testRun', dest='is_test_run', action="store_true", default=False, required=False)
args = parser.parse_args()
mode = args.DL_or_SL

if args.DL_or_SL == "DL":
    print "Starting dilepton analysis"
    indir = "test_trees/DL_trees/"

if args.DL_or_SL == "SL":
    print "Starting single lepton analysis"
    indir = "test_trees/SL_trees/"


f_all = {}
t_all_mc = {}
for sample in input_files:
    if mode == "DL" and (sample[:6] == "single"):
        continue
    if mode == "SL" and (sample[:2] == "di"):
        continue
    print "Opening sample: " + sample
    f_all[sample] = ROOT.TFile(indir + input_files[sample])
    t_all_mc[sample] = f_all[sample].Get("tree")

#f_all_data = {}
#t_all_data = {}
#for datasample in input_files_data:
#    print "Opening data sample: " + datasample
#    f_all_data[datasample] = ROOT.TFile(indir + input_files_data[datasample])
#    t_all_data[datasample] = f_all_data[datasample].Get("tree")


report_every = 100000
if args.is_test_run:
    max_event = 10000
else:
    max_event = -1

hists = {} #histograms for each sample and variable
for proc, tree in t_all_mc.iteritems():
    print "Processing: " + proc + " tree with " + str(tree.GetEntries()) + "events"
    
    hists[proc] = initialize_histograms(proc, hist_variables) # dictionary of initialized histograms for each sample
    vd = initialize_tree(tree, var_list) # dictionary of variables

    nr_tot, nr_pass_lep, nr_is_lep, nr_pass_jet, nr_pass_trigger = 0, 0, 0, 0, 0
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
            weight = ev_weight*tr_weight*pu_weight*19/12

        #-------------select events---------------
        nr_tot+=weight

        if proc[-7:] == "Mu_data" and not( pass_trigger_selection(vd, mode, "mu") ): continue
        if proc[-7:] == "El_data" and not( pass_trigger_selection(vd, mode, "el") ): continue
        nr_pass_trigger+=weight

        if vd["nLep"][0] < 1:continue
        nr_is_lep+=weight

        sel_lep = pass_lepton_selection(vd, mode)
        if len(sel_lep) == 0: continue
        nr_pass_lep+=weight

        sel_jet = pass_jet_selection(vd, mode)
        if len(sel_jet) == 0: continue
        nr_pass_jet+=weight

        hists[proc]["MET_pt"].Fill(vd["MET_pt"][0], weight)
        hists[proc]["lepton_pt"].Fill(vd["lepton_pt"][0], weight)
 
        hists[proc]["MET_phi"].Fill(vd["MET_phi"][0], weight)
        hists[proc]["jet_pt"].Fill(vd["jet_pt"][ sel_jet[0] ], weight)
#        hists[proc]["numJets"].Fill( len(sel_jet), weight)
        hists[proc]["numJets"].Fill( vd["numJets"][0], weight)

        hists[proc]["btag_LR"].Fill(vd["btag_LR"][ sel_jet[0] ], weight)
        
        hists[proc]["numBTagL"].Fill(vd["numBTagL"][0], weight)
        hists[proc]["numBTagM"].Fill(vd["numBTagM"][0], weight)
        hists[proc]["numBTagT"].Fill(vd["numBTagT"][0], weight)
        hists[proc]["nPVs"].Fill(vd["nPVs"][0], weight)

        if vd["lepton_type"][sel_lep[0]] == 13 :
            hists[proc]["muon_pt"].Fill(vd["lepton_pt"][sel_lep[0]], weight)
            hists[proc]["muon_eta"].Fill(vd["lepton_eta"][sel_lep[0]], weight)
            hists[proc]["muon_rIso"].Fill(vd["lepton_rIso"][sel_lep[0]], weight)
        else: 
            hists[proc]["electron_pt"].Fill(vd["lepton_pt"][sel_lep[0]], weight)
            hists[proc]["electron_eta"].Fill(vd["lepton_eta"][sel_lep[0]], weight)
            hists[proc]["electron_rIso"].Fill(vd["lepton_rIso"][sel_lep[0]], weight)
        #---------------------------------------

    print "Nr tot = "+ str(nr_tot)
    print "Nr trig sel = " + str(nr_pass_trigger)
    print "Nr is lep  = " + str(nr_is_lep)
    print "Nr lep sel = " + str(nr_pass_lep)
    print "Nr jet sel = " + str(nr_pass_jet)


outfilename = "histograms_" + mode + ".root"
write_histograms_to_file(outfilename, hists)

        
        
        


        
        
