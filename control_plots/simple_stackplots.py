import ROOT, sys, os
from histlib import hist_variables, variable_names, colors, set_file_name
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='mode',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
parser.add_argument('--sel', dest='sel', choices=["presel","presel_2b"], required=True, help="Specify the preselection level" )
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
parser.add_argument('--notopw', dest="notopw", action="store_true", default=False, required=False) # dont apply toppt weight    
args = parser.parse_args()

mode = args.mode
sel = args.sel
mctrig = not args.notrig
topw = not args.notopw

inclusive_ttjets = False

if sel == "presel_2b":
    selstr = "presel_2b_" # "2b_"
if sel == "presel":
    selstr = "presel"

signal_scale = 100
if sel == "presel_2b":
    signal_scale = 50

indir = "histograms/"

if mode=="SL":
    infile = set_file_name("histograms_presel_2b_SL", mctrig, topw)
if mode=="DL":
    infile = set_file_name("histograms_presel_2b_DL", mctrig, topw)

h = ROOT.TFile(indir + infile)
mc = {}

if mode == "DL":
    nrebin = 2
else:
    nrebin = 1

for hist in hist_variables:
    hist_to_plot = hist
    print "Plotting histogram for variable: " + hist_to_plot
    
    if mode=="SL":
        data_mu = h.Get("singleMu_data/" + hist_to_plot + "_singleMu_data")
        data_el = h.Get("singleEl_data/" + hist_to_plot + "_singleEl_data")
        data = data_mu.Clone("data")
        data.Add(data_el)
        if not (hist_to_plot[:3] == "num"):
            data.Rebin(nrebin)


    if mode=="DL":
        data_mu = h.Get("diMu_data/" + hist_to_plot + "_diMu_data")
        data_el = h.Get("diEl_data/" + hist_to_plot + "_diEl_data")
        data = data_mu.Clone("data")
        data.Add(data_el)
        if not(hist_to_plot[:3] == "num"):
            data.Rebin(nrebin)

    from odict import OrderedDict as dict
    mc = dict()

    mc["EWK"] = h.Get("EWK/" + hist_to_plot + "_EWK") # 
    mc["SingleTop"] = h.Get("SingleT/" + hist_to_plot + "_SingleT")
    mc["DiBoson"] = h.Get("DiBoson/" + hist_to_plot + "_DiBoson")
    mc["TTV"] = h.Get("TTV/" + hist_to_plot + "_TTV")

    if inclusive_ttjets:
        mc["TTJets"] = h.Get("TTJets/" + hist_to_plot + "_TTJets")
    else:
        mc["ttjj"] = h.Get("ttjj/" + hist_to_plot + "_ttjj")
        mc["ttb"] = h.Get("ttb/" + hist_to_plot + "_ttb")
        mc["ttbb"] = h.Get("ttbb/" + hist_to_plot + "_ttbb")
    mc["TTH125"] = h.Get("ttH125/" + hist_to_plot + "_ttH125")

    for key in mc:
        print "Starting MC process: " + key
        if not (hist_to_plot[:3] == "num"):
            mc[key].Rebin(nrebin)
        mc[key].SetLineColor(colors[key])
        mc[key].SetFillColor(colors[key])
        mc[key].SetFillStyle(1001)


    signal = mc["TTH125"].Clone("signal")
    signal.SetLineColor(ROOT.kBlue-3)
    signal.SetLineWidth(2)
    signal.SetFillStyle(0)
    signal.Scale(signal_scale)

#---------------- stacks -------------------------
    sum = ROOT.THStack("sum","")

    print "plotting histogram " + hist

    for key, sample in mc.iteritems():
        print "adding sample " + key + " to stack"
        sum.Add( sample )

    h_sumMC = mc["TTH125"].Clone("h_sumMC")
    for sample in mc:
        if sample is not "TTH125":
            h_sumMC.Add(mc[sample])
            
    h_sumMC.SetTitle("")  
    h_sumMC.SetStats(False)
    h_sumMC.SetLineWidth(2)
    h_sumMC.SetMaximum(1.3*max(h_sumMC.GetMaximum(), data.GetMaximum()) )
    h_sumMC.SetMinimum(0.)
    h_sumMC.SetLineColor(ROOT.kBlack)
    h_sumMC.SetFillStyle(0)
    h_sumMC.GetXaxis().SetTitle(variable_names[hist])

    data.SetMarkerColor(1)
    data.SetMarkerStyle(20)
    data.SetMarkerSize(1)

#---------------draw on canvas-------------------
    
    c = ROOT.TCanvas("c" + hist ,"c" + hist, 600, 600)
    
    h_sumMC.Draw("hist")
    sum.Draw("histsame")
    h_sumMC.Draw("histsame")
    mc["TTH125"].SetLineColor(ROOT.kBlack)
    signal.Draw("histsame")
    data.Draw("epsame")

#------------- legend ---------------------
    legend1 = ROOT.TLegend(0.64, 0.79, 0.89, 0.89, "", "brNDC")
    legend1.SetBorderSize(0)
    legend1.SetFillColor(0)
    legend1.AddEntry(data, "Data", "p")
    legend1.AddEntry(sum, "Expectation", "l")
    legend1.AddEntry(signal, "TTH125 x " + str(signal_scale) , "l")
    legend1.Draw()

    legend2 = ROOT.TLegend(0.64, 0.6, 0.89, 0.765, "", "brNDC")
    legend2.SetBorderSize(0)
    legend2.SetFillColor(0)
    
    mcitems = mc.items()
    mcitems.reverse()

    lmc = dict(mcitems)
    for lname, lh in lmc.iteritems():
        if not (lname == "TTH125"):
            legend2.AddEntry(lh, lname, "f")

    legend2.Draw()

#----------------------------------------------
    c.SaveAs("out_stackplots/" + mode + "/" + hist + "_" + selstr +".pdf")
    c.SaveAs("out_stackplots/" + mode + "/" + hist + "_" + selstr + ".png")
    c.Close()

