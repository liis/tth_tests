import sys
import ROOT
from histlib import fill_cut_flow, fill_cut_flow_bycut, set_file_name

indir = "histograms_test/"
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
    infile_DL = set_file_name("histograms_presel_2b_DL", mctrig, topw, noWeight)
else:
    infile_DL = set_file_name("histograms_presel_2b_DL", mctrig, topw, noWeight)

standalone = True

f_DL = ROOT.TFile(indir + infile_DL)

pars_DL = f_DL.Get("pars") # read lumi normalization of mc histograms
hist_lumi_DL = pars_DL.GetBinContent(pars_DL.GetXaxis().FindBin("Lumi") )

lf = 1 #19.5/hist_lumi # scale lumi to new value if needed, default 1
Lumi = hist_lumi_DL*lf

from odict import OrderedDict as dict
processes_MM = dict()
processes_MM["ttH125"] = f_DL.Get("ttH125/cut_flow_di_mu_ttH125")
processes_MM["ttjj"] = f_DL.Get("ttjj/cut_flow_di_mu_ttjj")
processes_MM["ttb"] = f_DL.Get("ttb/cut_flow_di_mu_ttb")
processes_MM["ttbb"] = f_DL.Get("ttbb/cut_flow_di_mu_ttbb")
processes_MM["TTV"] = f_DL.Get("TTV/cut_flow_di_mu_TTV")
processes_MM["SingleT"] = f_DL.Get("SingleT/cut_flow_di_mu_SingleT")
processes_MM["EWK"] = f_DL.Get("EWK/cut_flow_di_mu_EWK")
processes_MM["DiBoson"] = f_DL.Get("DiBoson/cut_flow_di_mu_DiBoson")

sumBkg_MM = processes_MM["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes_MM.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
        sumBkg_MM.Add(cf_hist)

data_MM = f_DL.Get("diMu_data/cut_flow_di_mu_diMu_data") # get cut-flow of data

processes_EE = dict()
processes_EE["ttH125"] = f_DL.Get("ttH125/cut_flow_di_ele_ttH125")
processes_EE["ttjj"] = f_DL.Get("ttjj/cut_flow_di_ele_ttjj")
processes_EE["ttb"] = f_DL.Get("ttb/cut_flow_di_ele_ttb")
processes_EE["ttbb"] = f_DL.Get("ttbb/cut_flow_di_ele_ttbb")
processes_EE["TTV"] = f_DL.Get("TTV/cut_flow_di_ele_TTV")
processes_EE["SingleT"] = f_DL.Get("SingleT/cut_flow_di_ele_SingleT")
processes_EE["EWK"] = f_DL.Get("EWK/cut_flow_di_ele_EWK")
processes_EE["DiBoson"] = f_DL.Get("DiBoson/cut_flow_di_ele_DiBoson")

sumBkg_EE = processes_EE["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes_EE.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
        sumBkg_EE.Add(cf_hist)
        

data_EE = f_DL.Get("diEl_data/cut_flow_di_ele_diEl_data")

processes_EM = dict()
processes_EM["ttH125"] = f_DL.Get("ttH125/cut_flow_emu_ttH125")
processes_EM["ttjj"] = f_DL.Get("ttjj/cut_flow_emu_ttjj")
processes_EM["ttb"] = f_DL.Get("ttb/cut_flow_emu_ttb")
processes_EM["ttbb"] = f_DL.Get("ttbb/cut_flow_emu_ttbb")
processes_EM["TTV"] = f_DL.Get("TTV/cut_flow_emu_TTV")
processes_EM["SingleT"] = f_DL.Get("SingleT/cut_flow_emu_SingleT")
processes_EM["EWK"] = f_DL.Get("EWK/cut_flow_emu_EWK")
processes_EM["DiBoson"] = f_DL.Get("DiBoson/cut_flow_emu_DiBoson")

sumBkg_EM = processes_EM["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes_EM.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
        sumBkg_EM.Add(cf_hist)

data_EM = f_DL.Get("diMu_data/cut_flow_emu_diMu_data") # get cut-flow of data   


cuts_DL = dict()
cuts_DL["DL1_tight"] = "DL"
#cuts_DL["cat7"] = "Cat. 7"

table_size = len(cuts_DL)

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
    print "*{3}{c|}",
print "}"
print "\\hline"
for cutlabel in cuts_DL.values():
    print " & \multicolumn{3}{|c|}{" + cutlabel + "}",
print '\\\ \\hline'

for cutlabel in cuts_DL:
    print "& $\mu\mu$ & $ee$ & $e\mu$", 
print '\\\ \\hline'    

tot_bkg = 0
for proc in processes_MM:
    print proc,

    for cut in cuts_DL:
        fill_cut_flow_bycut( processes_MM[proc], cut, lf, table_size, round_prec=2)
        fill_cut_flow_bycut( processes_EE[proc], cut, lf, table_size, round_prec=2)
        fill_cut_flow_bycut( processes_EM[proc], cut, lf, table_size, round_prec=2)

    print "\\\\"

print "\\hline"

#----------- sum bkg --------------
print "\\textbf{$\sum$ Bkg} ",

for cut in cuts_DL:
    fill_cut_flow_bycut(sumBkg_MM, cut, lf, table_size, bf = True)
    fill_cut_flow_bycut(sumBkg_EE, cut, lf, table_size, bf = True)
    fill_cut_flow_bycut(sumBkg_EM, cut, lf, table_size, bf = True)

print "\\\\"
print "\\hline"

#----------- data --------------------
print "\\textbf{Data} ",
for cut in cuts_DL:
    fill_cut_flow_bycut(data_MM, cut, lf, table_size, bf = True)
    fill_cut_flow_bycut(data_EE, cut, lf, table_size, bf = True)
    fill_cut_flow_bycut(data_EM, cut, lf, table_size, bf = True)
print "\\\\"
print "\\hline"
#--------------Total---------------------


#---------------------------------------
print """
        \end{tabular}
"""        
print "\caption{Cut flow in event categories for di-lepton topology (DL),",
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

