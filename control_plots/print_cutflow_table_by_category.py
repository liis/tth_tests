import sys
import ROOT
from histlib import fill_cut_flow, set_file_name

indir = "histograms/"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
parser.add_argument('--notopw', dest="notopw", action="store_true", default=False, required=False) # dont apply top pt weight
args = parser.parse_args()

mctrig = not args.notrig
topw = not args.notopw

#def set_file_name(file_name_base, mctrig, topw):
#    infile = file_name_base
#    if not mctrig:
#        infile = infile + "_notrig"
#    if not topw:
#        infile = infile + "_notopw"
#    infile = infile + ".root"
#    return infile

if not mctrig:
    infile_SL = set_file_name("histograms_presel_2b_SL", mctrig, topw)
    infile_DL = set_file_name("histograms_presel_2b_DL", mctrig, topw)
else:
    infile_SL = set_file_name("histograms_presel_2b_SL", mctrig, topw)
    infile_DL = set_file_name("histograms_presel_2b_DL", mctrig, topw)

standalone = True

f_SL = ROOT.TFile(indir + infile_SL)
f_DL = ROOT.TFile(indir + infile_DL)

pars_SL = f_SL.Get("pars") # read lumi normalization of mc histograms
pars_DL = f_DL.Get("pars")

hist_lumi_SL = pars_SL.GetBinContent(pars_SL.GetXaxis().FindBin("Lumi") )
hist_lumi_DL = pars_DL.GetBinContent(pars_DL.GetXaxis().FindBin("Lumi") )

if hist_lumi_SL != hist_lumi_DL:
    print "WARNING: lumi_SL != lumi_DL, using lumi_SL"

lf = 1 #19.5/hist_lumi # scale lumi to new value if needed, default 1
Lumi = hist_lumi_SL*lf

from odict import OrderedDict as dict
processes_SL = dict()
processes_SL["ttH125"] = f_SL.Get("ttH125/cut_flow_ttH125")
processes_SL["ttjj"] = f_SL.Get("ttjj/cut_flow_ttjj")
processes_SL["ttb"] = f_SL.Get("ttb/cut_flow_ttb")
processes_SL["ttbb"] = f_SL.Get("ttbb/cut_flow_ttbb")
processes_SL["TTV"] = f_SL.Get("TTV/cut_flow_TTV")
processes_SL["SingleT"] = f_SL.Get("SingleT/cut_flow_SingleT")
processes_SL["EWK"] = f_SL.Get("EWK/cut_flow_EWK")
processes_SL["DiBoson"] = f_SL.Get("DiBoson/cut_flow_DiBoson")

processes_DL = dict()
processes_DL["ttH125"] = f_DL.Get("ttH125/cut_flow_ttH125")
processes_DL["ttjj"] = f_DL.Get("ttjj/cut_flow_ttjj")
processes_DL["ttb"] = f_DL.Get("ttb/cut_flow_ttb")
processes_DL["ttbb"] = f_DL.Get("ttbb/cut_flow_ttbb")
processes_DL["TTV"] = f_DL.Get("TTV/cut_flow_TTV")
processes_DL["SingleT"] = f_DL.Get("SingleT/cut_flow_SingleT")
processes_DL["EWK"] = f_DL.Get("EWK/cut_flow_EWK")
processes_DL["DiBoson"] = f_DL.Get("DiBoson/cut_flow_DiBoson")

sumBkg_SL = processes_SL["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes_SL.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
        sumBkg_SL.Add(cf_hist)

sumBkg_DL = processes_DL["ttjj"].Clone("sumBkg") # Get a cut-flow histogram for sum Bkg
for proc, cf_hist in processes_DL.iteritems():
    if not proc == "ttH125" and not proc=="ttjj":
                sumBkg_DL.Add(cf_hist)

data_mu_SL = f_SL.Get("singleMu_data/cut_flow_singleMu_data") # get cut-flow of data
data_el_SL = f_SL.Get("singleEl_data/cut_flow_singleEl_data")
data_mu_DL = f_DL.Get("diMu_data/cut_flow_diMu_data") # get cut-flow of data
data_el_DL = f_DL.Get("diEl_data/cut_flow_diEl_data")

data_SL = data_mu_SL.Clone("data_SL")
data_SL.Add(data_el_SL)
data_DL = data_mu_DL.Clone("data_DL")
data_DL.Add(data_el_DL)

cuts_SL = dict()
cuts_SL["cat1"] = "Cat. 1"
cuts_SL["cat2"] = "Cat. 2"
cuts_SL["cat3_4"] = "Cat. 3/4"
cuts_SL["cat5"] = "Cat. 5"

cuts_DL = dict()
cuts_DL["cat6"] = "Cat. 6"
cuts_DL["cat7"] = "Cat. 7"

table_size = len(cuts_SL) + len(cuts_DL)

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
for it in range(table_size + 1):
    print "c|",
print "}"
print "\\hline"
for cutlabel in cuts_SL.values():
    print " & " + cutlabel,
for cutlabel in cuts_DL.values():
    print " & " + cutlabel,
print '\\\ \\hline'


tot_bkg = 0
for proc in processes_SL:
    print proc,
    fill_cut_flow(cuts_SL, processes_SL[proc], lf, table_size)
    fill_cut_flow(cuts_DL, processes_DL[proc], lf, table_size)

    print "\\\\"

print "\\hline"

#----------- sum bkg --------------
print "$\sum$ Bkg ",
fill_cut_flow(cuts_SL, sumBkg_SL, lf, table_size)
fill_cut_flow(cuts_DL, sumBkg_DL, lf, table_size)
print "\\\\"
print "\\hline"

#----------- data --------------------
print "Data ",
fill_cut_flow(cuts_SL, data_SL, lf, table_size)
fill_cut_flow(cuts_DL, data_DL, lf, table_size)
print "\\\\"
print "\\hline"
#-------------------------------------

print """
        \end{tabular}
"""        
print "\caption{Cut flow in event categories,",
print " L = " + str( round(Lumi, 2)) + " fb$^-1$",
if not mctrig:
    print " (no MC trigger applied) ",
print "}"
print """   
     \end{center}
        \end{table*}

        """
if standalone:
    print "\end{document}"

