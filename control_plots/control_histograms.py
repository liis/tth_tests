import ROOT, sys

from fill_jet_counts import fill_cut_flow, fill_jet_count_histograms, fill_btag_count_histograms, fill_category_count_histograms
from tree_inputs import input_files
from trlib import initialize_tree, var_list, pass_trigger_selection, pass_lepton_selection, pass_jet_selection, bjet_presel
from histlib import hist_variables, initialize_hist_ranges, initialize_histograms, fill_1D_histograms, fill_lepton_histograms, fill_jet_histograms, fill_single_histogram, write_histograms_to_file, event_count

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='DL_or_SL',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
parser.add_argument('--testRun', dest='is_test_run', action="store_true", default=False, required=False)
parser.add_argument('--sel', dest="sel", choices=["pre","pre_2b"], default=False, required=False)
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
parser.add_argument('--notopw', dest="notopw", action="store_true", default=False, required=False) # dont apply top pt reweight
parser.add_argument('--doSys', dest="doSys", action="store_true", default=False, required=False)
parser.add_argument('--noWeight', dest="noWeight", action="store_true", default=False, required=False)
parser.add_argument('--outdir', dest="outdir", default="./histograms_tests/")
                   
args = parser.parse_args()
mode = args.DL_or_SL
notopw=args.notopw

if args.DL_or_SL == "DL":
    print "Starting dilepton analysis"

if args.DL_or_SL == "SL":
    print "Starting single lepton analysis"
#indir = "test_trees/trees_2014_03_11_0-0-1_rec_std_withFixes_FinalOnly/" 
#indir = "test_trees/trees_2014_03_13_0-0-1_rec_std_fixed/"
#indir = "test_trees/trees_2014_03_17_0-0-1_rec_std_ttbarWeight/"
#indir = "test_trees/trees_2014_03_19_0-0-1_rec_std/"
#indir = "test_trees/trees_2014_03_25_0-0-1_rec_std/"
#indir = "test_trees/trees_2014_03_27_0-0-1_rec_std_sys/"
#indir = "test_trees/trees_2014_03_27_0-0-1_rec_std_final_sys_196/"
indir = "/home/bianchi/CMSSW_5_3_3_patch2/src/Bianchi/TTHStudies/root/"

print "Reading input from " + indir
print "Saving output to " + args.outdir

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
            
report_every = 2000
if args.is_test_run:
    max_event = 10000
else:
    max_event = -1

if args.doSys:
#    do_syst = ["", "_CSVup"]
    do_syst = ["","_CSVup","_CSVdown", "_JECup", "_JECdown", "_JERup", "_JERdown"] #
    print "Run systematic variations: " + str(do_syst)
else:
    do_syst = [""]
    print "Run nominal only"

hists = {} #histograms for each sample and variable

hist_variables = initialize_hist_ranges( mode, hist_variables )

for proc, tree in t_all.iteritems():
    print "Processing: " + proc + " tree with " + str(tree.GetEntries()) + "events"

    #---------------------------- initialize histograms---------------------------------
    isTTjets = False
    for isyst in do_syst:
        hists[proc + isyst] = initialize_histograms(proc, hist_variables, isyst) # dictionary of initialized histograms for each sample
        if proc == "TTJets": # initialize extra histograms for ttJets, separating by gen level decay
            isTTjets = True
            for sub_proc in ["ttbb", "ttb", "ttjj"]:
                hists[sub_proc + isyst] = initialize_histograms(sub_proc, hist_variables, isyst)

    #------------------------------------------------------------------------------------
    vd = initialize_tree(tree, var_list) # dictionary of variables

#    weights[proc] = ROOT.TH1F("weights_" + proc, "weights" + proc, 1, 0, 1)
#    if proc == "TTJets":
#        for sub_proc in ["ttbb", "ttb", "ttjj"]:
#            weights[sub_proc] = ROOT.TH1F("weights_" + sub_proc, "weights" + sub_proc, 1, 0, 1)
        
    weightsum = 0;    

    nr_evts = tree.GetEntries() 
    for i in range( nr_evts ):
        if i % report_every == 0:
            print "Event nr: " + str(i)
        if i == max_event and not i == -1: break

        tree.LoadTree(i)
        tree.GetEntry(i)
        #-----------------Check systematic variation-----------------
        idx_sys = vd["syst"][0] # index of syst uncertainty

        run_variation = False # Whether or not to run paricualr systematic variation
        for idx_runsys, isyst in enumerate(do_syst):
            if idx_runsys == idx_sys: run_variation = True
        if not run_variation: continue

#        print "running systematic" + do_syst[idx_sys]
        isyst = do_syst[idx_sys] # name of syst uncertainty
        #-----------------------------------------------------------
        
#        if proc == "TTJets":
#            print "PDF weight up = " + str( vd["SCALEsyst"][2] )
#            print "PDF weight down = " + str( vd["SCALEsyst"][3] )

        ev_weight = vd["weight"][0]
        weightsum += ev_weight
        
        tr_weight = vd["trigger"][0]
        pu_weight = vd["PUweight"][0]
        toppt_weight = vd["weightTopPt"][0]
        el_weight = vd["weightEle"][0]

        csv_weight = vd["weightCSV"][0] #corresponds to nominal
#        csv_weight = 1


        if proc[-4:] == "data":
            weight = 1
        else:
            weight = ev_weight*pu_weight*csv_weight*el_weight*Lumi/12.1
            if not notopw:
                weight = weight*toppt_weight
            if usetrig:
                weight = weight*tr_weight

        if args.noWeight:
            weight = 1
        #-------------Select events---------------

        
#        event_count(0, "all", cut_flow, proc, weight, vd, idx_sys) # cut-flow: all evts

        if proc[-7:] == "Mu_data"  and not( pass_trigger_selection(vd, mode, "mu") and ( (mode=="SL" and vd["Vtype"][0]==2) or (mode=="DL" and ( vd["Vtype"][0]==0 or vd["Vtype"][0]==4)) ) ): continue #combined trigger and lepton selection
        if proc[-7:] == "El_data" and not( pass_trigger_selection(vd, mode, "el") and ( (mode=="SL" and vd["Vtype"][0]==3) or (mode=="DL" and vd["Vtype"][0]==1)) ): continue
        if (proc[-7:] == "Mu_data" or proc[-7:] == "El_data") and idx_sys != 0: continue # Run nominal, skip systematic variations
        #        event_count(1, "trig", cut_flow, proc, weight, vd, idx_sys) # cut_flow: apply trigger for data FIXME

        sel_lep = pass_lepton_selection(vd, mode)
#        if not ( len(sel_lep) ): continue
        if not ( ( mode == "DL" and (vd["Vtype"][0] == 0 or vd["Vtype"][0] == 1 or vd["Vtype"][0] == 4)) or ( mode == "SL" and (vd["Vtype"][0] == 2 or vd["Vtype"][0]==3)) ): continue  #lepton selection

        if vd["hJetAmong"] < 2: continue; # additional quality check (should be done at tree production level)

       #------------------- fill cutflow histos -------------------------------
        fill_cut_flow("cut_flow", vd, hists, proc, isyst, weight, mode)
        if mode == "DL" and vd["Vtype"][0] == 0:
            fill_cut_flow("cut_flow_di_mu", vd, hists, proc, isyst, weight, mode)
        if mode == "DL" and vd["Vtype"][0] == 1:
            fill_cut_flow("cut_flow_di_ele", vd, hists, proc, isyst, weight, mode)
        if mode == "DL" and vd["Vtype"][0] == 4:
            fill_cut_flow("cut_flow_emu", vd, hists, proc, isyst, weight, mode)
        if mode == "SL" and vd["Vtype"][0] == 2:
            fill_cut_flow("cut_flow_smu", vd, hists, proc, isyst, weight, mode)
        if mode == "SL" and vd["Vtype"][0] == 3:
            fill_cut_flow("cut_flow_sele", vd, hists, proc, isyst, weight, mode)
        
        #-------------------jet count histograms - fill before preselection!---------------------
        sel_jet = pass_jet_selection(vd, mode, jet40=True)
        
        fill_jet_count_histograms(vd, hists, proc, isyst, weight, mode ) #FIXME put DL/SL dependent histogram ranges
        fill_btag_count_histograms(vd, hists, proc, isyst, weight )
        fill_category_count_histograms(vd, hists, proc, isyst, weight, mode )
        # btag-LR before preselection

        if ( mode == "SL" and vd["MET_pt"][0] > 30 ) or ( mode == "DL" and vd["mV"][0] > 15 ):
            if vd["numJets"][0] >= 4: #for dilepton
                fill_single_histogram(vd, "btag_LR_4j", vd["btag_LR"][0], hists, proc, isyst, weight)
            if vd["numJets"][0] == 5:
                fill_single_histogram(vd, "btag_LR_5j", vd["btag_LR"][0], hists, proc, isyst, weight)
            if vd["numJets"][0] >= 6:
                fill_single_histogram(vd, "btag_LR_6j", vd["btag_LR"][0], hists, proc, isyst, weight)


        if (mode == "SL" and vd["numJets"][0] >= 5 and vd["numBTagM"][0] >= 2) or (mode == "DL" and vd["numJets"][0] >= 2 and vd["numBTagM"][0] >= 2): 
            fill_1D_histograms( vd, hists, proc, isyst, weight, mode, isTTjets ) 
            fill_lepton_histograms( vd, hists, proc, isyst, weight, mode, sel_lep, isTTjets = isTTjets) 
            fill_jet_histograms(vd, hists, proc, isyst, weight, mode, isTTjets = isTTjets)


    if max_event <= 0:
        proc_evts = nr_evts
    else:
        proc_evts = max_event
    
    print "weightsum =", weightsum
    print "nr_evts = ", proc_evts
    hists[proc]["weights"].SetBinContent(1, weightsum/proc_evts)
    if proc == "TTJets":
        for sub_proc in ["ttbb", "ttb", "ttjj"]:
            hists[sub_proc]["weights"].SetBinContent(1, weightsum/proc_evts)

    print "weight = " + str(hists[proc]["weights"].GetBinContent(1))

    print "--------- PRINT CUT FLOW ------------- "
    print "Nr tot = "+  str(hists[proc]["cut_flow"].GetBinContent(1))
    print "Nr trig sel = " + str(hists[proc]["cut_flow"].GetBinContent(2))
    print "Nr lep sel = " + str(hists[proc]["cut_flow"].GetBinContent(3))

#    if mode == "SL":
#        print ">=6 jets + 2 tags: " + str(cut_flow[proc].GetBinContent(4))
#        print "--------------------"
#        print ">=6 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("Lg7j4t")) )
#        print "6 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L6j4t")) )
#        print "5 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L5j4t")) )

#        print "------------------"
#        print ">=6 jets + >4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("Lg7jg4t")))
#        print "6 jets + >4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L6jg4t")) )
#        print "5 jets + >4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L5jg4t")) )

#        print "------------------"
#        print "type 1: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat1")) )
#        print "type 2: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat2")) )
#        print "type 3/4: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat3_4")) )
#        print "type 5: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat5")) )

#    if mode == "DL":
#        print "g4j4t: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("g4j4t")) )
#        print "3M1L: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("3t1t")) )
#        print "type 6: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat6")) )
#        print "type 7: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("cat7")) )

sel = "presel_2b_"
outdir = args.outdir

outfilename = outdir + "histograms_" + sel + mode
if not usetrig:
    outfilename = outfilename + "_notrig" 
if notopw:
    outfilename = outfilename + "_notopw"
if args.doSys:
    outfilename = outfilename + "_withSys"
if args.is_test_run:
    outfilename = outfilename + "_test"
if args.noWeight:
    outfilename = outfilename + "_noWeight"

outfilename = outfilename + ".root"
    
print "Write output to file: " + outfilename 
write_histograms_to_file(outfilename, hists, [], [pars])

        
        


        
        
