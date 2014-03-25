import ROOT

infile_1 = "histograms/MEAnalysisNewTEST.root"
infile_2 = "histograms/MEAnalysisNewTEST_reg.root"

var = "Top" #H, Top

f1 = ROOT.TFile(infile_1)
f2 = ROOT.TFile(infile_2)

t1 = f1.Get("tree")
t2 = f2.Get("tree")

h1 = ROOT.TH1F("h1","h1", 100, 0, 250)
h2 = ROOT.TH1F("h2","h2", 100, 0, 250)

c = ROOT.TCanvas("c" ,"c", 600, 600)
c.SetGrid(1,1)

nRebin=2
tvar = "m" + var + "_matched"

t1.Draw("m" + var + "_matched>>h1")
t2.Draw("m" + var + "_matched>>h2")

h1.SetStats(False)
h1.SetTitle("")
h1.GetXaxis().SetTitle("Higgs" + " mass" )


h2.SetStats(False)

h1.SetLineWidth(2)
h2.SetLineWidth(2)

h1.SetLineColor(ROOT.kBlue-3)
h2.Scale(1./h2.Integral())

h1.Rebin(nRebin)
h2.Rebin(nRebin)

h1.Scale(1./h1.Integral())
h2.SetLineColor(ROOT.kRed-3)

h1.SetMaximum(1.1*max(h1.GetMaximum(), h2.GetMaximum()) )

print "Mean value nominal = " + str(h1.GetMean())
print "RMS value nominal = " + str(h1.GetRMS())
print "Mean value reg = " + str(h2.GetMean())
print "RMS value nominal = " + str(h2.GetRMS())

h1.Draw()
h2.Draw("same")

legend = ROOT.TLegend(0.64, 0.79, 0.89, 0.89, "", "brNDC")
legend.SetBorderSize(0)
legend.SetFillColor(0)

legend.AddEntry(h1, "nominal","l")
legend.AddEntry(h2, "b-regression","l")
legend.Draw()

outfilename ="m" + var + "_reg.pdf"
c.SaveAs(outfilename)
