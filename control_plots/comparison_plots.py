import ROOT, sys, os
import tdrstyle
tdrstyle.tdrstyle()
from histlib import initialize_variable_names, variable_names, colors, set_file_name, get_ratio
from systematics import find_sum_sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='mode',  choices=["DL", "SL"], required=True, help="specify DL or SL analysis")
parser.add_argument('--sel', dest='sel', default="presel_2b", required=False, help="Specify the preselection level" )
parser.add_argument('--notrig', dest="notrig", action="store_true", default=False, required=False) # dont apply trigger on MC sel
parser.add_argument('--notopw', dest="notopw", action="store_true", default=False, required=False) # dont apply toppt weight    
parser.add_argument('--doSys', dest="doSys", action="store_true", default=False, required=False) # draw with systematics band
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

indir = "histograms_LRplot/"

if mode=="SL":
    infile = set_file_name("histograms_presel_2b_SL", mctrig, topw, args.doSys)
if mode=="DL":
    infile = set_file_name("histograms_presel_2b_DL", mctrig, topw, args.doSys)

print "opening input file:" + indir + infile

h = ROOT.TFile(indir + infile)
mc = {}

if mode == "DL":
    nrebin = 1
else:
    nrebin = 1


for hist in variable_names:
    hist_to_plot = hist

#-----------------------------systematics--------------------------------
    if args.doSys: #dictionary for sys variation of each process
        sys_up = find_sum_sys(h, ["CSVup", "JECup", "JERup"], hist)

    print "Plotting histogram for variable: " + hist_to_plot
    
    if mode=="SL":
        data_mu = h.Get("singleMu_data/" + hist_to_plot + "_singleMu_data")
        data_el = h.Get("singleEl_data/" + hist_to_plot + "_singleEl_data")
        data = data_mu.Clone("data")
        data.Add(data_el)
        if not (hist_to_plot[:3] == "num" or hist_to_plot[-5:] == "count"):
            data.Rebin(nrebin)


    if mode=="DL":
        data_mu = h.Get("diMu_data/" + hist_to_plot + "_diMu_data")
        data_el = h.Get("diEl_data/" + hist_to_plot + "_diEl_data")
        data = data_mu.Clone("data")
        data.Add(data_el)
        if not(hist_to_plot[:3] == "num" or hist_to_plot[-5:] == "count"):
            data.Rebin(nrebin)

    from odict import OrderedDict as dict
    mc = dict()

    mc["TTH125"] = h.Get("ttH125/" + hist_to_plot + "_ttH125")
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
    
    for key in mc:
        print "Starting MC process: " + key
        if not (hist_to_plot[:3] == "num" or hist_to_plot[-5:] == "count"):
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
        if not key=="TTH125":
            print "adding sample " + key + " to stack"
            sum.Add( sample )

    h_sumMC = mc["TTV"].Clone("h_sumMC")
    for sample in mc:
        if not sample=="TTH125" and not sample=="TTV":
            h_sumMC.Add(mc[sample])


    if args.doSys: #dictionary for sys variation of each process
        sys_up = find_sum_sys(h, ["CSVup", "JECup", "JERup"], hist, nrebin)
        sys_down = find_sum_sys(h, ["CSVdown", "JECdown", "JERdown"], hist, nrebin)

#        if not(hist_to_plot[:3] == "num" or hist_to_plot[-5:] == "count"):
#            sys_down.Rebin(nrebin)
#            sys_up.Rebin(nrebin)
            
        sys_up.Add(h_sumMC) # add total MC systematic to sumMC

        sys_down.Scale(-1)
        sys_down.Add(h_sumMC)

    
    h_sumMC.SetTitle("")  
    h_sumMC.SetStats(False)
    h_sumMC.SetLineWidth(2)
    h_sumMC.SetMaximum(1.3*max(h_sumMC.GetMaximum(), data.GetMaximum()) )
    h_sumMC.SetMinimum(0.)
    h_sumMC.SetLineColor(ROOT.kBlack)
    h_sumMC.SetFillStyle(0)
    h_sumMC.GetXaxis().SetTitle( initialize_variable_names(variable_names, mode)[hist])

    data.SetMarkerColor(1)
    data.SetMarkerStyle(20)
    data.SetMarkerSize(1)

    c = ROOT.TCanvas("c" + hist ,"c" + hist, 800, 1000)
    p1 = ROOT.TPad("p1", "p1", 0, 0.25, 1, 1)
    p1.SetBottomMargin(0)

    if hist == "jet_count" or hist == "btag_count" or hist == "cat_count":
        p1.SetLogy()    
    
    p1.Draw()
    p1.SetTicks(1, 1);

    p1.SetFillStyle(0);
    p1.cd()
    
    if hist == "jet_count" or hist == "btag_count" or hist == "cat_count":
        h_sumMC.SetMinimum(1)
        h_sumMC.SetMaximum(3.6*ROOT.TMath.Max(h_sumMC.GetMaximum(), data.GetMaximum()) )
        sum.SetMinimum(0.01)
        mc["TTH125"].SetMinimum(0.01)
        signal.SetMinimum(0.01)
        data.SetMinimum(0.01)
    
    h_sumMC.Draw("hist")
    sum.Draw("histsame")
    h_sumMC.Draw("histsame")
    mc["TTH125"].SetLineColor(ROOT.kBlack)
    signal.Draw("histsame")
    data.Draw("epsame")

    #---legend---
    legend1 = ROOT.TLegend(0.7, 0.78, 0.9, 0.89, "", "brNDC")
    legend1.SetBorderSize(0)
    legend1.SetFillColor(0)
    legend1.AddEntry(data, "Data", "p")
    legend1.AddEntry(sum, "Expectation", "l")
    legend1.AddEntry(signal, "TTH125 x " + str(signal_scale) , "l")
    legend1.Draw()
    
    legend2 = ROOT.TLegend(0.7, 0.55, 0.9, 0.765, "", "brNDC")
    legend2.SetBorderSize(0)
    legend2.SetFillColor(0)
    
    mcitems = mc.items()
    mcitems.reverse()
    
    lmc = dict(mcitems)
    for lname, lh in lmc.iteritems():
        if not (lname == "TTH125"):
            legend2.AddEntry(lh, lname, "f")
            
    legend2.Draw()     

    c.cd()
    #--------------
    
    p2 = ROOT.TPad("p2","p2", 0, 0.02, 1, 0.18)
    p2.SetTopMargin(0.0)
    p2.SetGrid();
    p2.SetFillStyle(0);
    p2.Draw()
    p2.cd()

    #--------------

    hist_ratio = get_ratio(data, h_sumMC, "Data/MC")
    hist_ratio.Draw("p0e1")
    if args.doSys:
        hist_ratio_up = get_ratio(sys_up, h_sumMC)
        hist_ratio_down = get_ratio(sys_down, h_sumMC)

   #     gr_up = ROOT.TGraph(2);   
   #     gr_up.SetHistogram(hist_ratio_up)
   #     gr_up.Draw()
     
        hist_ratio_up.Draw("histsame")
        hist_ratio_down.Draw("histsame")

    c.cd()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.03)
    latex.SetTextAlign(31)
    latex.SetTextAlign(11)


    cut = "5 jets + 2 b-tags"
    if mode=="SL":
        cut = "1 lep. + " + cut
    if mode=="DL":
        cut = "2 lep. + " + cut
        
    std_txt = "   #sqrt{s}=8 TeV, L=19.04 fb^{-1}"
    
    textlabel = std_txt
#    if topw:
#        textlabel = cut + ", (with top p_{T} SF)" + std_txt
    latex.DrawLatex(0.15, 0.975, textlabel)

    c.SaveAs("out_stackplots/" + mode + "/" + hist + "_" + selstr +".pdf")
    c.SaveAs("out_stackplots/" + mode + "/" + hist + "_" + selstr + ".png")
    c.Close()   
