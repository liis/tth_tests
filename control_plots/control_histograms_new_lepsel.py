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
                   
args = parser.parse_args()
mode = args.DL_or_SL
notopw=args.notopw

if args.DL_or_SL == "DL":
    print "Starting dilepton analysis"

if args.DL_or_SL == "SL":
    print "Starting single lepton analysis"

##indir = "test_trees/trees_2014_02_09_0-0-1_rec_std/"
#indir = "test_trees/trees_2014_02_15_0-0-1_rec_std/"
#indir = "test_trees/trees_2014_02_25_0-0-1_rec_std/" # syst set to 1
#indir = "test_trees/trees_2014_03_11_0-0-1_rec_std/"
#indir = "test_trees/trees_2014_03_11_0-0-1_rec_std_oldV2/"
indir = "test_trees/trees_2014_03_11_0-0-1_rec_std_withFixes_FinalOnly/" # missing cat 1,2

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
    max_event = 30000
else:
    max_event = -1

if args.doSys:
#    do_syst = ["", "_CSVup"]
    do_syst = ["","_CSVup","_CSVdown", "_JECup", "_JECdown", "_JERup", "_JERdown"] #
else:
    do_syst = [""]

hists = {} #histograms for each sample and variable
cut_flow = {}
cut_flow_di_mu = {}
cut_flow_di_ele = {}
cut_flow_emu = {}
cut_flow_smu = {}
cut_flow_sele = {}

#jet_count_hist = {}
#btag_count_hist = {}
#category_count_hist = {}

hist_variables = initialize_hist_ranges( mode, hist_variables )

for proc, tree in t_all.iteritems():
    print "Processing: " + proc + " tree with " + str(tree.GetEntries()) + "events"

    #---------------------------- initialize histograms---------------------------------
    isTTjets = False
    for isyst in do_syst:
        hists[proc + isyst] = initialize_histograms(proc, hist_variables, isyst) # dictionary of initialized histograms for each sample
        cut_flow[proc + isyst] = ROOT.TH1F("cut_flow_" + proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
        cut_flow_di_mu[proc + isyst] = ROOT.TH1F("cut_flow_di_mu_" + proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
        cut_flow_di_ele[proc + isyst] = ROOT.TH1F("cut_flow_di_ele_" + proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
        cut_flow_emu[proc + isyst] = ROOT.TH1F("cut_flow_emu_" + proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
        cut_flow_smu[proc + isyst] = ROOT.TH1F("cut_flow_smu_" + proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
        cut_flow_sele[proc + isyst] = ROOT.TH1F("cut_flow_sele_" + proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )

        cut_flow[proc + isyst].Sumw2()
        cut_flow_di_mu[proc + isyst].Sumw2()
        cut_flow_di_ele[proc + isyst].Sumw2()
        cut_flow_emu[proc + isyst].Sumw2()
        cut_flow_smu[proc + isyst].Sumw2()
        cut_flow_sele[proc + isyst].Sumw2()
        
        if proc == "TTJets": # initialize extra histograms for ttJets, separating by gen level decay
            isTTjets = True
            for sub_proc in ["ttbb", "ttb", "ttjj"]:
                hists[sub_proc + isyst] = initialize_histograms(sub_proc, hist_variables, isyst)
                cut_flow[sub_proc + isyst] = ROOT.TH1F("cut_flow_" + sub_proc + isyst, "cut_flow_" + sub_proc, 35, 0, 35)
                cut_flow_di_mu[sub_proc + isyst] = ROOT.TH1F("cut_flow_di_mu_" + sub_proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
                cut_flow_di_ele[sub_proc + isyst] = ROOT.TH1F("cut_flow_di_ele_" + sub_proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
                cut_flow_emu[sub_proc + isyst] = ROOT.TH1F("cut_flow_emu_" + sub_proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
                cut_flow_smu[sub_proc + isyst] = ROOT.TH1F("cut_flow_smu_" + sub_proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )
                cut_flow_sele[sub_proc + isyst] = ROOT.TH1F("cut_flow_sele_" + sub_proc + isyst, "cut_flow_" + proc + isyst, 35, 0 , 35 )

                cut_flow[sub_proc + isyst].Sumw2()
                cut_flow_di_mu[sub_proc + isyst].Sumw2()
                cut_flow_di_ele[sub_proc + isyst].Sumw2()
                cut_flow_emu[sub_proc + isyst].Sumw2()
                cut_flow_smu[sub_proc + isyst].Sumw2()
                cut_flow_sele[sub_proc + isyst].Sumw2()
    #------------------------------------------------------------------------------------
    vd = initialize_tree(tree, var_list) # dictionary of variables

    for i in range( tree.GetEntries() ):
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
        
        ev_weight = vd["weight"][0]
        tr_weight = vd["trigger"][0]
        pu_weight = vd["PUweight"][0]
        toppt_weight = vd["weightTopPt"][0]
        
        if proc[-4:] == "data":
            weight = 1
        else:
            weight = ev_weight*pu_weight*Lumi/12.1
            if not notopw:
                weight = weight*toppt_weight
            if usetrig:
                weight = weight*tr_weight

        if args.noWeight:
            weight = 1
        #-------------Select events---------------

        
        event_count(0, "all", cut_flow, proc, weight, vd, idx_sys) # cut-flow: all evts

        if proc[-7:] == "Mu_data"  and not( pass_trigger_selection(vd, mode, "mu") and ( (mode=="SL" and vd["Vtype"][0]==2) or (mode=="DL" and ( vd["Vtype"][0]==0 or vd["Vtype"][0]==4)) ) ): continue #combined trigger and lepton selection
        if proc[-7:] == "El_data" and not( pass_trigger_selection(vd, mode, "el") and ( (mode=="SL" and vd["Vtype"][0]==3) or (mode=="DL" and vd["Vtype"][0]==1)) ): continue
        if (proc[-7:] == "Mu_data" or proc[-7:] == "El_data") and idx_sys != 0: continue # Run nominal, skip systematic variations

        #        event_count(1, "trig", cut_flow, proc, weight, vd, idx_sys) # cut_flow: apply trigger for data FIXME

#        if not ( len(sel_lep) ): continue
        if not ( ( mode == "DL" and (vd["Vtype"][0] == 0 or vd["Vtype"][0] == 1 or vd["Vtype"][0] == 4))
                 or ( mode == "SL" and (vd["type"][0] == 2 or vd["type"][0]==3)) ): continue #FIXME -- uncomment for control plots

       #------------------- fill cutflow histos -------------------------------
        fill_cut_flow(cut_flow, proc, weight, vd, mode, idx_sys=0)
        if mode == "DL" and vd["Vtype"][0] == 0:
            fill_cut_flow(cut_flow_di_mu, proc, weight, vd, mode, idx_sys=0)
        if mode == "DL" and vd["Vtype"][0] == 1:
            fill_cut_flow(cut_flow_di_ele, proc, weight, vd, mode, idx_sys=0)
        if mode == "DL" and vd["Vtype"][0] == 4:
            fill_cut_flow(cut_flow_emu, proc, weight, vd, mode, idx_sys=0)
        if mode == "SL" and vd["Vtype"][0] == 2:
            fill_cut_flow(cut_flow_smu, proc, weight, vd, mode, idx_sys=0)
        if mode == "SL" and vd["Vtype"][0] == 3:
            fill_cut_flow(cut_flow_sele, proc, weight, vd, mode, idx_sys=0)
        
        #-------------------jet count histograms - fill before preselection!---------------------
        sel_jet = pass_jet_selection(vd, mode, jet40=True)
        
        fill_jet_count_histograms(vd, hists, proc, isyst, weight, mode ) #FIXME put DL/SL dependent histogram ranges
        fill_btag_count_histograms(vd, hists, proc, isyst, weight )
        fill_category_count_histograms(vd, hists, proc, isyst, weight, mode )
        # btag-LR before preselection
        if vd["numJets"][0] == 4:
            fill_single_histogram(vd, "btag_LR_4j", vd["btag_LR"][0], hists, proc, isyst, weight)
        if vd["numJets"][0] == 5:
            fill_single_histogram(vd, "btag_LR_5j", vd["btag_LR"][0], hists, proc, isyst, weight)
        if vd["numJets"][0] == 6:
            fill_single_histogram(vd, "btag_LR_6j", vd["btag_LR"][0], hists, proc, isyst, weight)
        if vd["numJets"][0] >= 7: 
            fill_single_histogram(vd, "btag_LR_7j", vd["btag_LR"][0], hists, proc, isyst, weight)


        if (mode == "SL" and vd["numJets"][0] >= 5 and vd["numBTagM"][0] >= 2) or (mode == "DL" and vd["numJets"][0] >= 2 and vd["numBTagM"][0] >= 2): 
#            fill_1D_histograms( vd, hists, proc, isyst, weight, mode, isTTjets ) 
#            fill_lepton_histograms( vd, hists, proc, isyst, weight, mode, sel_lep, isTTjets)
             fill_jet_histograms(vd, hists, proc, isyst, weight, mode, isTTjets = isTTjets)

    print "--------- PRINT CUT FLOW ------------- "
    print "Nr tot = "+  str(cut_flow[proc].GetBinContent(1))
    print "Nr trig sel = " + str(cut_flow[proc].GetBinContent(2))
    print "Nr lep sel = " + str(cut_flow[proc].GetBinContent(3))

    if mode == "SL":
        print ">=6 jets + 2 tags: " + str(cut_flow[proc].GetBinContent(4))
        print "--------------------"
        print ">=6 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("Lg7j4t")) )
        print "6 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L6j4t")) )
        print "5 jets + 4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L5j4t")) )

        print "------------------"
        print ">=6 jets + >4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("Lg7jg4t")))
        print "6 jets + >4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L6jg4t")) )
        print "5 jets + >4 tags: " + str(cut_flow[proc].GetBinContent(cut_flow[proc].GetXaxis().FindBin("L5jg4t")) )

        print "------------------"
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
if args.doSys:
    outfilename = outfilename + "_withSys"
if args.is_test_run:
    outfilename = outfilename + "_test"
if args.noWeight:
    outfilename = outfilename + "_noWeight"

outfilename = outfilename + ".root"
    
print "Write output to file: " + outfilename 
write_histograms_to_file(outfilename, hists, [cut_flow, cut_flow_di_mu, cut_flow_di_ele, cut_flow_emu, cut_flow_smu, cut_flow_sele], [pars])

        
        


        
        
