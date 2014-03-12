import ROOT, sys
from histlib import event_count

def fill_cut_flow(cut_flow_hists, proc, weight, vd, mode, idx_sys = 0):
    """
    fill cut flow histogram at selections of interest
    cut_flow_hist -- dictionary of initialized cut_flow histograms for each process
    """

    event_count(2, "lep. sel.", cut_flow_hists, proc, weight, vd, idx_sys)

    if vd["numJets"][0] >= 5 and vd["numBTagM"][0] >= 2: # SL preselection
        event_count(3, "presel_SL", cut_flow_hists, proc, weight, vd, idx_sys ) 

    if vd["numJets"][0] >=4 and vd["numBTagM"][0] >=2: # DL preselection
        event_count(4, "presel_DL", cut_flow_hists, proc, weight, vd, idx_sys )

    if vd["numJets"][0] >= 6 and vd["numBTagM"][0] == 2:
        event_count(5, "g6j2t", cut_flow_hists, proc, weight, vd, idx_sys )

    if vd["numJets"][0] == 5 and vd["numBTagM"][0] == 3:
        event_count(6, "5j3t", cut_flow_hists, proc,weight, vd, idx_sys)
        
    if vd["numJets"][0] >=6 and vd["numBTagM"][0] == 3:
        event_count(7, "g6j3t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numJets"][0] == 4 and vd["numBTagM"][0] ==4:
        event_count(8, "4j4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numBTagM"][0] ==4:
        event_count(9, "g4j4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=4:
        event_count(10, "5jg4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numJets"][0] >=6 and vd["numBTagM"][0] >=4:
        event_count(11, "g6jg4t", cut_flow_hists, proc,weight, vd, idx_sys)

    #------lorenzo categories-----------

    if vd["numJets"][0] ==6 and vd["numBTagM"][0] >=4: # cat 1, 2
        event_count(12, "L6jg4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numJets"][0] >= 7 and vd["numBTagM"][0] >= 4: # cat 5
        event_count(13, "Lg7jg4t", cut_flow_hists, proc, weight, vd, idx_sys)

    if vd["numJets"][0] ==5 and vd["numBTagM"][0] >= 4: # cat 3, 4
        event_count(14, "L5jg4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numJets"][0] ==6 and vd["numBTagM"][0] ==4: # cat 1, 2
        event_count(15, "L6j4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numJets"][0] >= 7 and vd["numBTagM"][0] == 4: # cat 5
        event_count(16, "Lg7j4t", cut_flow_hists, proc, weight, vd, idx_sys)

    if vd["numJets"][0] ==5 and vd["numBTagM"][0] == 4: # cat 3, 4
        event_count(17, "L5j4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numBTagM"][0] >=4:
        event_count(18, "g4t", cut_flow_hists, proc,weight, vd, idx_sys)

    if vd["numBTagM"][0] ==3 and vd["numBTagL"][0]==4:
        event_count(19, "3t1t", cut_flow_hists, proc,weight, vd, idx_sys)

    #--------------For DL---------------------
#    if vd["numJets"][0] >=4 and vd["numBTagM"][0] == 1:
#        event_count(20, "4j2t", cut_flow, proc, weight,vd, idx_sys)

#    if vd["numJets"][0] >=4 and vd["numBTagM"][0]==2:
#        event_count(21, "g4j2t", cut_flow, proc, weight,vd, idx_sys)

#    if vd["numBTagM"][0]>=3:
#        event_count(22, "g3t", cut_flow, proc, weight,vd, idx_sys)

    #------according to event type --------
    if vd["type"][0] == 0:
        event_count(23, "cat1", cut_flow_hists, proc, weight, vd, idx_sys)
    if vd["type"][0] == 1:
        event_count(24, "cat2", cut_flow_hists, proc, weight, vd, idx_sys)
    if vd["type"][0] == 2:
        event_count(25, "cat3_4", cut_flow_hists, proc, weight, vd, idx_sys)
    if vd["type"][0] == 3:
        event_count(26, "cat5", cut_flow_hists, proc, weight,vd, idx_sys)
    if vd["type"][0] == 6:
        event_count(27, "cat6", cut_flow_hists, proc, weight,vd, idx_sys)
    if vd["type"][0] == 7:
        event_count(28, "cat7", cut_flow_hists, proc, weight,vd, idx_sys)
    
    if vd["type"][0] == 2 and vd["flag_type2"][0] == 2:
        event_count(29, "cat3", cut_flow_hists, proc, weight, vd, idx_sys)
    if vd["type"][0] ==2 and vd["flag_type2"][0] != 2:
        event_count(30, "cat4", cut_flow_hists, proc, weight, vd, idx_sys)

            
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

        elif vd["numJets"][0] ==9 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["jet_count"].GetXaxis().SetBinLabel( 7, "10j")
            hists[proc + syst]["jet_count"].Fill(6, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "jet_count", 6, "10j", syst, weight)


def fill_btag_count_histograms(vd, hists, proc, syst, weight):
    if vd["numBTagM"][0] ==2:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 1, "2 b-tag")
        hists[proc + syst]["btag_count"].Fill(0, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 0, "2 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] ==3:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 2, "3 b-tag")
        hists[proc + syst]["btag_count"].Fill(1, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 1, "3 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] ==4:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 3, "4 b-tag")
        hists[proc + syst]["btag_count"].Fill(2, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 2, "4 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] >=5:
        hists[proc + syst]["btag_count"].GetXaxis().SetBinLabel( 4, ">4 b-tag")
        hists[proc + syst]["btag_count"].Fill(3, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, hists, "btag_count", 3, "5 b-tag", syst, weight)
            
def fill_category_count_histograms(vd, hists, proc, syst, weight, mode):

    if mode == "SL":
        if vd["numJets"][0] >=5 and vd["numBTagM"][0] >=2:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 1, ">4j >1t")
            hists[proc + syst]["category_count"].Fill(0, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 0, ">4j >1t", syst, weight)
        
        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=4:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 2, "5j >3t")
            hists[proc + syst]["category_count"].Fill(1, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 1, ">5j >3t", syst, weight)
        
        if vd["numJets"][0] == 6 and vd["numBTagM"][0] >=4:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 3, "6j >3t")
            hists[proc + syst]["category_count"].Fill(2, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 2, "6j >3t", syst, weight)
        
        if vd["numJets"][0] == 7 and vd["numBTagM"][0] >=4:
            hists[proc + syst]["category_count"].GetXaxis().SetBinLabel( 4, ">7j >3t")
            hists[proc + syst]["category_count"].Fill(3, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, hists, "category_count", 3, ">7j >3t", syst, weight)

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
                                        
