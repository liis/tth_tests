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
    indir = "test_trees/DL_trees/"

if args.DL_or_SL == "SL":
    print "Starting single lepton analysis"
    indir = "test_trees/SL_trees/"


f_all = {}
t_all_mc = {}
for sample in input_files:
    if mode == "DL" and (sample[:6] == "single"): continue
    if mode == "SL" and (sample[:2] == "di"): continue
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
cut_flow = {}
for proc, tree in t_all_mc.iteritems():
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
            weight = ev_weight*pu_weight*19/12*tr_weight

        #-------------select events---------------
        
        event_count(0, cut_flow, proc, weight, vd)

        if proc[-7:] == "Mu_data" and not( pass_trigger_selection(vd, mode, "mu") ): continue
        if proc[-7:] == "El_data" and not( pass_trigger_selection(vd, mode, "el") ): continue
        event_count(1, cut_flow, proc, weight, vd)

        sel_lep = pass_lepton_selection(vd, mode) # count the number of good electrons and apply preselection
        sel_jet = pass_jet_selection(vd, mode) # count the number of good jets and apply preselection
        bjets_m = bjet_presel(vd, jet_list = sel_jet, WP = "M") # count the number of b-jets CSV medium

        if len(sel_lep) == 0: continue
        event_count(2, cut_flow, proc, weight, vd)

        if len(sel_jet) == 0: continue
        event_count(3, cut_flow, proc, weight, vd)

 #       if( vd["jet_eta"][sel_jet[0]] < 0.01 and  vd["jet_eta"][sel_jet[0]] > -0.01 ):
 #           print "jet pt = " + str(vd["jet_pt"][sel_jet[0]]) + ", jet phi = " + str(vd["jet_phi"][sel_jet[0]]) + ", jet eta = " + str(vd["jet_eta"][sel_jet[0]])

        if len(sel_jet) >= 6 and len(bjets_m) >= 2: # SL preselection
            event_count(4, cut_flow, proc, weight, vd)
        else: continue
        
        if len(sel_jet) >= 6 and len(bjets_m) >= 4: # an SL type0, type1
            event_count(5, cut_flow, proc, weight, vd)
#        else: continue

        if vd["flag_type0"][0] >= 0:
            event_count(6, cut_flow, proc, weight, vd)

#        if len(sel_jet) > 6 and len(bjets_m) == 4: # an SL type3
#            event_count(6, cut_flow, proc, weight, vd)

 #       if len(sel_jet) ==5 and len(bjets_m) == 4: #an type2
 #           event_count(7, cut_flow, proc, weight, vd)


  #      fill_1D_histograms( vd, hists, proc, weight, mode, isTTjets )
  #      fill_lepton_histograms( vd, hists, proc, weight, mode, sel_lep, isTTjets)
        fill_jet_histograms(vd, hists, proc, weight, mode, sel_jet, isTTjets)
  #      hists[proc]["numBTagM_sel"].Fill(len(bjets_m), weight)
  #      hists[proc]["numJets_sel"].Fill(len(sel_jet), weight)

        #---------------------------------------

    

    #------ Fill cut flow histogram---------

   # cut_flow[proc].SetBinContent(0, nr_tot)
   # cut_flow[proc].SetBinContent(1, nr_pass_trigger)
   # cut_flow[proc].SetBinContetn(2, nr_pass_lep)
   # cut_flow[proc].SetBinContent(3, nr_pass_jet)

    print "--------- CUT FLOW ------------- "
    print "Nr tot = "+  str(cut_flow[proc].GetBinContent(1))
    print "Nr trig sel = " + str(cut_flow[proc].GetBinContent(2))
    print "Nr lep sel = " + str(cut_flow[proc].GetBinContent(3))
    print "Nr jet sel = " + str(cut_flow[proc].GetBinContent(4))
    print "SL presel  = " + str(cut_flow[proc].GetBinContent(5))
    print ">6 jets > 4 tag = " + str(cut_flow[proc].GetBinContent(6))
    print "vtype0 or vtype1 " + str(cut_flow[proc].GetBinContent(7))

#    print "5 jets 4 tag = " + str(cut_flow[proc].GetBinContent(8))

sel = "presel_2b_"
outfilename = "histograms_" + sel + mode + ".root"
print "Write output to file: " + outfilename 


write_histograms_to_file(outfilename, hists, cut_flow)
#for proc in cut_flow:
#    cut_flow[proc].Write()
        
        
        


        
        
