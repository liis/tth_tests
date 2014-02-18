## Needs work !! ##

import ROOT
from trlib import initialize_tree, var_list

indir =  "/Users/liis/Desktop/tests/check_data/"
 
infile1 = "MEAnalysisNew_nominal_0-0-1_rec_std_Run2012_SingleElectronRun2012C-EcalRecover_11Dec2012-v1_v2_p1.root"
infile2 = "MEAnalysisNew_nominal_0-0-1_rec_std_Run2012_SingleElectronRun2012CPromptv2.root"

f1 = ROOT.TFile(indir + infile1)
f2 = ROOT.TFile(indir + infile2)

t1 = f1.Get("tree")
t2 = f2.Get("tree")

vd1 = initialize_tree(t1, var_list)
vd2 = initialize_tree(t2, var_list)

run_ev_lumi_1 = []
run_ev_lumi_2 = []

for i in range( t1.GetEntries() ):
    t1.LoadTree(i)
    t1.GetEntry(i)
    print vd1
#    rev = (vd1["EVENT.run"][0], vd1["EVENT.event"][0], vd1["EVENT.lumi"][0])
#    run_ev_lumi_1.append(rev)

print run_ev_lumi_1
    
