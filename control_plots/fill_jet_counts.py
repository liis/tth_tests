import ROOT, sys
from histlib import event_count


def fill_cut_flow( cut_flow_name, vd, hists, proc, syst, weight, mode ): 
    if mode == "SL":
        if vd["numJets"][0] == 5:
            hists[proc + syst][ cut_flow_name].GetXaxis().SetBinLabel(1, "SL cat. 1")
            hists[proc + syst][ cut_flow_name].Fill(0, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, cut_flow_name, 0, "SL cat. 1", syst, weight)
            
        elif vd["numJets"][0] >= 6:
            hists[proc + syst][ cut_flow_name].GetXaxis().SetBinLabel(2, "SL cat. 2")
            hists[proc + syst][ cut_flow_name].Fill(1, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, cut_flow_name, 1, "SL cat. 2", syst, weight)

            
def fill_ttjets_histograms_singlevar( vd, hists, histname, nbin, binlabel, syst, weight ):
    """
    Apply gen level filter to separate subprocesses of ttjj. Seva histograms separately
    """
    if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
        hists["ttbb" + syst][histname].GetXaxis().SetBinLabel( nbin+1, binlabel)
        hists["ttbb" + syst][histname].Fill(nbin, weight)
        
    elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
        hists["ttb" + syst][histname].GetXaxis().SetBinLabel( nbin+1, binlabel)
        hists["ttb" + syst][histname].Fill(nbin, weight)
        
    elif vd["nSimBs"][0] == 2:
        hists["ttjj" + syst][histname].GetXaxis().SetBinLabel( nbin+1, binlabel)
        hists["ttjj" + syst][histname].Fill(nbin, weight)

def fill_jet_count_histograms(vd, hists, proc, syst, weight, mode):

    if mode == "DL":
        if vd["numJets"][0] ==4 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 1, "4j")
            hists[proc + syst]["jet_count"].Fill(0, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 0, "4j", syst, weight)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 2, "5j")
            hists[proc + syst]["jet_count"].Fill(1, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 1, "5j", syst, weight)

        if vd["numJets"][0] ==6 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 3, "6j")
            hists[proc + syst]["jet_count"].Fill(2, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 2, "6j", syst, weight)

        if vd["numJets"][0] ==7 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 4, "7j")
            hists[proc + syst]["jet_count"].Fill(3, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 3, "7j", syst, weight)
                                                                
    
                
    if mode == "SL":
        if vd["numJets"][0] ==4 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 1, "4j")
            hists[proc + syst]["jet_count"].Fill(0, weight)
   
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 0, "4j", syst, weight)
        
        elif vd["numJets"][0] ==5 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 2, "5j")
            hists[proc + syst]["jet_count"].Fill(1, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 1, "5j", syst, weight)

        elif vd["numJets"][0] ==6 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 3, "6j")
            hists[proc + syst]["jet_count"].Fill(2, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count",  2, "6j", syst, weight)

        elif vd["numJets"][0] ==7 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 4, "7j")
            hists[proc + syst]["jet_count"].Fill(3, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 3, "7j", syst, weight)
        
        elif vd["numJets"][0] ==8 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 5, "8j")
            hists[proc + syst]["jet_count"].Fill(4, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 4, "8j", syst, weight)
                
        elif vd["numJets"][0] ==9 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 6, "9j")
            hists[proc + syst]["jet_count"].Fill(5, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 5, "9j", syst, weight)

        elif vd["numJets"][0] == 10 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 7, "10j")
            hists[proc + syst]["jet_count"].Fill(6, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 6, "10j", syst, weight)


def fill_btag_count_histograms(vd, hists, proc, syst, weight):
    if vd["numBTagM"][0] ==2:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 1, "0 b-tag")
        hists[proc + syst]["btag_count"].Fill(0, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 0, "0 b-tag", syst, weight)

    if vd["numBTagM"][0] ==1:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 2, "1 b-tag")
        hists[proc + syst]["btag_count"].Fill(1, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 1, "1 b-tag", syst, weight)

    if vd["numBTagM"][0] ==2:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 3, "2 b-tag")
        hists[proc + syst]["btag_count"].Fill(2, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 2, "2 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] ==3:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 4, "3 b-tag")
        hists[proc + syst]["btag_count"].Fill(3, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 3, "3 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] ==4:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 5, "4 b-tag")
        hists[proc + syst]["btag_count"].Fill(4, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 4, "4 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] >=5:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 6, ">4 b-tag")
        hists[proc + syst]["btag_count"].Fill(5, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 5, "5 b-tag", syst, weight)
            
def fill_category_count_histograms(vd, hists, proc, syst, weight, mode):

    if mode == "SL":
        if vd["numJets"][0] >=5 and vd["numBTagM"][0] >=4:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 1, "all")
            hists[proc + syst]["category_count"].Fill(0, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 0, "all", syst, weight)
        
        if vd["numJets"][0] >=6 and vd["numBTagM"][0] >=4:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 2, "SL cat. 1")
            hists[proc + syst]["category_count"].Fill(1, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 1, "SL cat. 1", syst, weight)
        
        if vd["numJets"][0] >= 6 and vd["numBTagM"][0] >=4:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 3, "SL cat. 2")
            hists[proc + syst]["category_count"].Fill(2, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 2, "SL cat. 2", syst, weight)
        
        if vd["numJets"][0] == 5 and vd["numBTagM"][0] >=4:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 4, "SL cat. 3")
            hists[proc + syst]["category_count"].Fill(3, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 3, "SL cat. 3", syst, weight)

    if mode=="DL":
        if vd["numJets"][0] >=4 and vd["numBTagM"][0] >2:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 3, ">3j >2t")
            hists[proc + syst]["category_count"].Fill(2, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 2, ">3j >2t", syst, weight)

        if vd["numJets"][0] >=4 and vd["numBTagM"][0] ==2:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 2, ">3j 2t")
            hists[proc + syst]["category_count"].Fill(1, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 1, ">3j 2t", syst, weight)

        if vd["numJets"][0] < 4 and vd["numBTagM"][0] ==2:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 1, ">3j 2t")
            hists[proc + syst]["category_count"].Fill(0, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 0, "<4j 2t", syst, weight)
                                        
