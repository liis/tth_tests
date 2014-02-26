import ROOT, sys

def fill_ttjets_histograms_singlevar( vd, hists, varname, var, weight ):
    """
    Apply gen level filter to separate subprocesses of ttjj. Seva histograms separately
    """
    if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
        hists["ttbb"][varname].Fill(var, weight)
        
    elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
        hists["ttb"][varname].Fill(var, weight)
        
    elif vd["nSimBs"][0] == 2:
        hists["ttjj"][varname].Fill(var, weight)

def fill_jet_count_histograms(vd, jet_count_hists, proc, weight):

    if vd["numJets"][0] >=4:
        jet_count_hists[proc].GetXaxis().SetBinLabel( 1, "4j")
        jet_count_hists[proc].Fill(0, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, jet_count_hists, 1, weight)
        
