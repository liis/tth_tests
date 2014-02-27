import sys
import ROOT
from histlib import fill_cut_flow, set_file_name

indir = "histograms/"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
parser.add_argument('--notopw', dest="notopw", action="store_true", default=False, required=False) # dont apply top pt weight
args = parser.parse_args()

sys = False
mode = "SL"
mctrig = not args.notrig
topw = not args.notopw

if mode == "SL":
    infile = set_file_name("histograms_presel_2b_SL", mctrig, topw, sys)
elif mode == "DL":
    infile = set_file_name("histograms_presel_2b_DL", mctrig, topw, sys)

standalone = True

f = ROOT.TFile(indir + infile)

pars = f.Get("pars") # read lumi normalization of mc histograms
hist_lumi = pars.GetBinContent(pars.GetXaxis().FindBin("Lumi") )
lf = 1 #19.5/hist_lumi # scale lumi to new value if needed, default 1
Lumi = hist_lumi*lf

from odict import OrderedDict as dict
processes = dict()
processes["ttH125"] = f.Get("ttH125/cut_flow_ttH125")
processes["ttjj"] = f.Get("ttjj/cut_flow_ttjj")
processes["ttb"] = f.Get("ttb/cut_flow_ttb")
processes["ttbb"] = f.Get("ttbb/cut_flow_ttbb")
processes["TTV"] = f.Get("TTV/cut_flow_TTV")
processes["SingleT"] = f.Get("SingleT/cut_flow_SingleT")
processes["EWK"] = f.Get("EWK/cut_flow_EWK")
processes["DiBoson"] = f.Get("DiBoson/cut_flow_DiBoson")

sumBkg = processes["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
        sumBkg.Add(cf_hist)

if mode == "SL":
    data_mu = f.Get("singleMu_data/cut_flow_singleMu_data") # get cut-flow of data
    data_el = f.Get("singleEl_data/cut_flow_singleEl_data")
if mode == "DL":
    danta_mu = f.Get("diMu_data/cut_flow_diMu_data") # get cut-flow of data
    data_el = f.Get("diEl_data/cut_flow_diEl_data")

data = data_mu.Clone("data")
data.Add(data_el)


cuts_ttHbl_SL = dict() # processes for labels in cut-flow histograms
cuts_ttHbl_SL["g6j2t"] =  "$\ge$6j 2t"
cuts_ttHbl_SL["4j3t"] =  "4j 3t"
cuts_ttHbl_SL["5j3t"] = "5j 3t"
cuts_ttHbl_SL["g6j3t"] = "$\ge$6j 3t"
cuts_ttHbl_SL["4j4t"] = "4j 4t"
cuts_ttHbl_SL["5jg4t"] = "5j $\ge$ 4t"
cuts_ttHbl_SL["g6jg4t"] = "$\ge$6j $\ge$ 4t"

cuts_L_SL = dict()
cuts_L_SL["cat1"] = "Cat. 1"
cuts_L_SL["cat2"] = "Cat. 2"
cuts_L_SL["cat3_4"] = "Cat. 3/4"
cuts_L_SL["cat5"] = "Cat. 5"

cuts_L_SL["L6j4t"] = "6j 4t"
cuts_L_SL["L5j4t"] = "5j 4t"
cuts_L_SL["Lg7j4t"] = "$\ge$7j 4t"

#cuts_L_SL["L6jg4t"] = "6j $\ge$4t"
#cuts_L_SL["L5jg4t"] = "5j $\ge$4t"
#cuts_L_SL["Lg7jg4t"] = "$\ge$7j $\ge$4t"

cuts_L_DL = dict()
cuts_L_DL["4j2t"] = "4j 2t"
cuts_L_DL["4j3t"] = "4j 3t" 
cuts_L_DL["4j4t"] = "4j $\ge$4t"


if mode == "SL":
    cuts = cuts_ttHbl_SL

elif mode == "DL":
    cuts = cuts_L_DL
else:
    print "Specify SL or DL"
    sys.exit()

table_size = len(cuts)

if standalone:
    print "\documentclass{article}"
    print "\usepackage[landscape]{geometry}"
    print "\\begin{document}"

print """
        \\begin{table*}[htbp]
        \\begin{center}"""

print "\label{tab:cutflow}"
#print "\scriptsize{"
print "\\begin{tabular}{|",
for it in range(len(cuts) + 1):
    print "c|",
print "}"
print "\\hline"
for cutlabel in cuts.values():
    print " & " + cutlabel,
print '\\\ \\hline'


tot_bkg = 0
for proc, proc_cf in processes.iteritems():
    print proc,
    fill_cut_flow(cuts, proc_cf, lf)
    print "\\\\"
print "\\hline"

#----------- sum bkg --------------
print "$\sum$ Bkg ",
fill_cut_flow(cuts, sumBkg, lf)
print "\\\\"
print "\\hline"

#----------- data --------------------
print "Data ",
fill_cut_flow(cuts, data, lf)
print "\\\\"
print "\\hline"
#-------------------------------------

print """
        \end{tabular}
"""        
print "\caption{Cut flow,",
if mode == "SL":
    print "SL selection, ",
elif mode == "DL":
    print "DL selection, ",
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

