import sys
import ROOT
from histlib import fill_cut_flow, fill_cut_flow_bycut, set_file_name

indir = "histograms/"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
parser.add_argument('--notopw', dest="notopw", action="store_true", default=False, required=False) # dont apply top pt weight
parser.add_argument('--noWeight', dest="noWeight", action="store_true", default=False, required=False)
args = parser.parse_args()

mctrig = not args.notrig
topw = not args.notopw
noWeight = args.noWeight

if not mctrig:
    infile_SL = set_file_name("histograms_presel_2b_SL", mctrig, topw, noWeight)
else:
    infile_SL = set_file_name("histograms_presel_2b_SL", mctrig, topw, noWeight)

standalone = True

f_SL = ROOT.TFile(indir + infile_SL)

pars_SL = f_SL.Get("pars") # read lumi normalization of mc histograms
hist_lumi_SL = pars_SL.GetBinContent(pars_SL.GetXaxis().FindBin("Lumi") )

lf = 1 #19.5/hist_lumi # scale lumi to new value if needed, default 1
Lumi = hist_lumi_SL*lf

from odict import OrderedDict as dict
processes_SM = dict()
processes_SM["ttH125"] = f_SL.Get("ttH125/cut_flow_smu_ttH125")
processes_SM["ttjj"] = f_SL.Get("ttjj/cut_flow_smu_ttjj")
processes_SM["ttb"] = f_SL.Get("ttb/cut_flow_smu_ttb")
processes_SM["ttbb"] = f_SL.Get("ttbb/cut_flow_smu_ttbb")
processes_SM["TTV"] = f_SL.Get("TTV/cut_flow_smu_TTV")
processes_SM["SingleT"] = f_SL.Get("SingleT/cut_flow_smu_SingleT")
processes_SM["EWK"] = f_SL.Get("EWK/cut_flow_smu_EWK")
processes_SM["DiBoson"] = f_SL.Get("DiBoson/cut_flow_smu_DiBoson")

sumBkg_SM = processes_SM["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes_SM.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
        sumBkg_SM.Add(cf_hist)

data_SM = f_SL.Get("singleMu_data/cut_flow_smu_singleMu_data") # get cut-flow of data


processes_SE = dict()
processes_SE["ttH125"] = f_SL.Get("ttH125/cut_flow_sele_ttH125")
processes_SE["ttjj"] = f_SL.Get("ttjj/cut_flow_sele_ttjj")
processes_SE["ttb"] = f_SL.Get("ttb/cut_flow_sele_ttb")
processes_SE["ttbb"] = f_SL.Get("ttbb/cut_flow_sele_ttbb")
processes_SE["TTV"] = f_SL.Get("TTV/cut_flow_sele_TTV")
processes_SE["SingleT"] = f_SL.Get("SingleT/cut_flow_sele_SingleT")
processes_SE["EWK"] = f_SL.Get("EWK/cut_flow_sele_EWK")
processes_SE["DiBoson"] = f_SL.Get("DiBoson/cut_flow_sele_DiBoson")

sumBkg_SE = processes_SE["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes_SE.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
        sumBkg_SE.Add(cf_hist)
        

data_SE = f_SL.Get("singleEl_data/cut_flow_sele_singleEl_data")

#data_SL = data_mu_SL.Clone("data_SL")
#data_SL.Add(data_el_SL)

cuts_SL = dict()
cuts_SL["cat1"] = "Cat. 1"
cuts_SL["cat2"] = "Cat. 2"
cuts_SL["cat3_4"] = "Cat. 3/4"
cuts_SL["cat5"] = "Cat. 5"


table_size = len(cuts_SL)

if standalone:
    print "\documentclass{article}"
    print "\usepackage[landscape]{geometry}"
    print "\\begin{document}"

print """
        \\begin{table*}[htbp]
        \\begin{center}"""

print "\label{tab:cutflow}"
#print "\scriptsize{"
print "\\begin{tabular}{|l|",
for it in range(table_size + 1):
    print "*{2}{c|}",
print "}"
print "\\hline"
for cutlabel in cuts_SL.values():
    print " & \multicolumn{2}{|c|}{" + cutlabel + "}",
print '\\\ \\hline'

for cutlabel in cuts_SL:
    print "& muon & electron", 
print '\\\ \\hline'    

tot_bkg = 0
for proc in processes_SM:
    print proc,

    for cut in cuts_SL:
        fill_cut_flow_bycut( processes_SM[proc], cut, lf, table_size)
        fill_cut_flow_bycut( processes_SE[proc], cut, lf, table_size)

    print "\\\\"

print "\\hline"

#----------- sum bkg --------------
print "\\textbf{$\sum$ Bkg} ",

for cut in cuts_SL:
    fill_cut_flow_bycut(sumBkg_SM, cut, lf, table_size, bf = True)
    fill_cut_flow_bycut(sumBkg_SE, cut, lf, table_size, bf = True)
print "\\\\"
print "\\hline"

#----------- data --------------------
print "\\textbf{Data} ",
for cut in cuts_SL:
    fill_cut_flow_bycut(data_SM, cut, lf, table_size, bf = True)
    fill_cut_flow_bycut(data_SE, cut, lf, table_size, bf = True)
print "\\\\"
print "\\hline"
#-------------------------------------

print """
        \end{tabular}
"""        
print "\caption{Cut flow in event categories for lepton + jet topology (SL),",
print " L = " + str( round(Lumi, 2)) + " fb$^{-1}$",
if not mctrig:
    print " (no MC trigger applied) ",
print "}"
print """   
     \end{center}
        \end{table*}

        """
if standalone:
    print "\end{document}"

