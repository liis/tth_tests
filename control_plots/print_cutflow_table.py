import ROOT
from histlib import fill_cut_flow

indir = "histograms/"
infile = "histograms_presel_2b_SL.root"
standalone = True

f = ROOT.TFile(indir + infile)

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

data_mu = f.Get("singleMu_data/cut_flow_singleMu_data") # get cut-flow of data
data_el = f.Get("singleEl_data/cut_flow_singleEl_data")
data = data_mu.Clone("data")
data.Add(data_el)


cuts_ttHbl_SL = dict() # processes for labels in cut-flow histograms
cuts_ttHbl_SL["g6j2t"] =  "$\ge$6j 2t"
cuts_ttHbl_SL["4j3t"] =  "4j 3t"
cuts_ttHbl_SL["g6j3t"] = "$\ge$6j 3t"
cuts_ttHbl_SL["5jg4t"] = "$\ge$5j 4t"
cuts_ttHbl_SL["g6jg4t"] = "$\ge$6j $\ge$ 4t"

cuts = cuts_ttHbl_SL
table_size = len(cuts)

if standalone:
    print "\documentclass{article}"
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
    print proc + " & ",
    fill_cut_flow(cuts, proc_cf)

print "\\hline"

#----------- sum bkg --------------
print "$\sum$ Bkg & ",
fill_cut_flow(cuts, sumBkg)

print "\\hline"

#----------- data --------------------
print "Data & ",
fill_cut_flow(cuts, data)

print "\\hline"
#-------------------------------------

print """
        \end{tabular}

        \caption{Cut flow}
        \end{center}
        \end{table*}

        """

if standalone:
    print "\end{document}"

