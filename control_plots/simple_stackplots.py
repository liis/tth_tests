import ROOT, sys, os
from histlib import hist_variables, variable_names, colors
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='mode',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
args = parser.parse_args()

mode = args.mode

if mode=="SL":
    infile = "./histograms_SL.root"
if mode=="DL":
    infile = "./histograms_DL.root"

h = ROOT.TFile(infile)
mc = {}
nrebin = 1

for hist in hist_variables:
    hist_to_plot = hist
    print "Plotting histogram for variable: " + hist_to_plot
    
    if mode=="SL":
        data_mu = h.Get("singleMu_data/" + hist_to_plot + "_singleMu_data")
        data_el = h.Get("singleEl_data/" + hist_to_plot + "_singleEl_data")
        data = data_mu.Clone("data")
        data.Add(data_el)



    if mode=="DL":
        data_mu = h.Get("diMu_data/" + hist_to_plot + "_diMu_data")
        data_el = h.Get("diEl_data/" + hist_to_plot + "_diEl_data")
        data = data_mu.Clone("data")
        data.Add(data_el)

    from odict import OrderedDict as dict
    mc = dict()

    mc["EWK"] = h.Get("EWK/" + hist_to_plot + "_EWK")
    mc["SingleTop"] = h.Get("SingleT/" + hist_to_plot + "_SingleT")
    mc["DiBoson"] = h.Get("DiBoson/" + hist_to_plot + "_DiBoson")
    mc["TTV"] = h.Get("TTV/" + hist_to_plot + "_TTV")
    mc["TTJets"] = h.Get("TTJets/" + hist_to_plot + "_TTJets")
    mc["TTH125"] = h.Get("ttH125/" + hist_to_plot + "_ttH125")

    for key in mc:
        print "Starting MC process: " + key
        mc[key].Rebin(nrebin)
        mc[key].SetLineColor(colors[key])
        mc[key].SetFillColor(colors[key])
        mc[key].SetFillStyle(1001)
    mc["TTH125"].SetLineColor(ROOT.kBlack)
        
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
    data.Draw("epsame")

#------------- legend ---------------------
    legend1 = ROOT.TLegend(0.64, 0.79, 0.89, 0.89, "", "brNDC")
    legend1.SetBorderSize(0)
    legend1.SetFillColor(0)
    legend1.AddEntry(data, "Data", "p")
    legend1.AddEntry(sum, "Expectation", "l")
    legend1.Draw()

    legend2 = ROOT.TLegend(0.64, 0.515, 0.89, 0.765, "", "brNDC")
    legend2.SetBorderSize(0)
    legend2.SetFillColor(0)
    
    mcitems = mc.items()
    mcitems.reverse()
    lmc = dict(mcitems)

    for lname, lh in lmc.iteritems():
        legend2.AddEntry(lh, lname, "f")
    legend2.Draw()

#----------------------------------------------
    c.SaveAs("out_stackplots/" + mode + "/" + hist + ".pdf")
    c.SaveAs("out_stackplots/" + mode + "/" + hist + ".png")
    c.Close()

