import ROOT, sys

def fill_ttjets_histograms_singlevar( vd, hists, nbin, binlabel, syst, weight ):
    """
    Apply gen level filter to separate subprocesses of ttjj. Seva histograms separately
    """
    if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
        hists["ttbb" + syst].GetXaxis().SetBinLabel( nbin+1, binlabel)
        hists["ttbb" + syst].Fill(nbin, weight)
        
    elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
        hists["ttb" + syst].GetXaxis().SetBinLabel( nbin+1, binlabel)
        hists["ttb" + syst].Fill(nbin, weight)
        
    elif vd["nSimBs"][0] == 2:
        hists["ttjj" + syst].GetXaxis().SetBinLabel( nbin+1, binlabel)
        hists["ttjj" + syst].Fill(nbin, weight)

def fill_jet_count_histograms(vd, jet_count_hists, proc, syst, weight, mode):

    if mode == "DL": #additional selection for njets
#        if vd["numJets"][0] ==2 and vd["numBTagM"][0] >=2:
#            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 1, "2j")
#            jet_count_hists[proc + syst].Fill(0, weight)
            
#            if proc[:6] == "TTJets":
#                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 0, "2j", syst, weight)

#        if vd["numJets"][0] ==3 and vd["numBTagM"][0] >=2:
#            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 2, "3j")
#            jet_count_hists[proc + syst].Fill(1, weight)
#            
#            if proc[:6] == "TTJets":
#                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 1, "3j", syst, weight)

        if vd["numJets"][0] ==4 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 1, "4j")
            jet_count_hists[proc + syst].Fill(0, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 0, "4j", syst, weight)

        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 2, "5j")
            jet_count_hists[proc + syst].Fill(1, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 1, "5j", syst, weight)

        if vd["numJets"][0] ==6 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 3, "6j")
            jet_count_hists[proc + syst].Fill(2, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 2, "6j", syst, weight)

        if vd["numJets"][0] ==7 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 4, "7j")
            jet_count_hists[proc + syst].Fill(3, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 3, "7j", syst, weight)
                                                                
    
                
    if mode == "SL":
        if vd["numJets"][0] ==4 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 1, "4j")
            jet_count_hists[proc + syst].Fill(0, weight)
   
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 0, "4j", syst, weight)
        
        elif vd["numJets"][0] ==5 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 2, "5j")
            jet_count_hists[proc + syst].Fill(1, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 1, "5j", syst, weight)

        elif vd["numJets"][0] ==6 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 3, "6j")
            jet_count_hists[proc + syst].Fill(2, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 2, "6j", syst, weight)

        elif vd["numJets"][0] ==7 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 4, "7j")
            jet_count_hists[proc + syst].Fill(3, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 3, "7j", syst, weight)
        
        elif vd["numJets"][0] ==8 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 5, "8j")
            jet_count_hists[proc + syst].Fill(4, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 4, "8j", syst, weight)
                
        elif vd["numJets"][0] ==9 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 6, "9j")
            jet_count_hists[proc + syst].Fill(5, weight)

            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 5, "9j", syst, weight)

        elif vd["numJets"][0] ==9 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 7, "10j")
            jet_count_hists[proc + syst].Fill(6, weight)
            
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 6, "10j", syst, weight)


def fill_btag_count_histograms(vd, jet_count_hists, proc, syst, weight):
    if vd["numBTagM"][0] ==2:
        jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 1, "2 b-tag")
        jet_count_hists[proc + syst].Fill(0, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, jet_count_hists, 0, "2 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] ==3:
        jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 2, "3 b-tag")
        jet_count_hists[proc + syst].Fill(1, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, jet_count_hists, 1, "3 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] ==4:
        jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 3, "4 b-tag")
        jet_count_hists[proc + syst].Fill(2, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, jet_count_hists, 2, "4 b-tag", syst, weight)
        
    elif vd["numBTagM"][0] ==5:
        jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 4, "5 b-tag")
        jet_count_hists[proc + syst].Fill(3, weight)
        if proc[:6] == "TTJets":
            fill_ttjets_histograms_singlevar(vd, jet_count_hists, 3, "5 b-tag", syst, weight)
            
#    elif vd["numBTagM"][0] ==6:
#        jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 5, "6 b-tag")
#        jet_count_hists[proc + syst].Fill(4, weight)
#        if proc[:6] == "TTJets":
#            fill_ttjets_histograms_singlevar(vd, jet_count_hists, 4, "6 b-tag", syst, weight)

def fill_category_count_histograms(vd, jet_count_hists, proc, syst, weight, mode):

    if mode == "SL":
        if vd["numJets"][0] >=5 and vd["numBTagM"][0] >=2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 1, ">4j >1t")
            jet_count_hists[proc + syst].Fill(0, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 0, ">4j >1t", syst, weight)
        
        if vd["numJets"][0] ==5 and vd["numBTagM"][0] >=4:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 2, "5j >3t")
            jet_count_hists[proc + syst].Fill(1, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 1, ">5j >3t", syst, weight)
        
        if vd["numJets"][0] == 6 and vd["numBTagM"][0] >=4:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 3, "6j >3t")
            jet_count_hists[proc + syst].Fill(2, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 2, "6j >3t", syst, weight)
        
        if vd["numJets"][0] == 7 and vd["numBTagM"][0] >=4:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 4, ">7j >3t")
            jet_count_hists[proc + syst].Fill(3, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 3, ">7j >3t", syst, weight)




    if mode=="DL":
        if vd["numJets"][0] >=4 and vd["numBTagM"][0] >2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 3, ">3j >2t")
            jet_count_hists[proc + syst].Fill(2, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 2, ">3j >2t", syst, weight)

        if vd["numJets"][0] >=4 and vd["numBTagM"][0] ==2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 2, ">3j 2t")
            jet_count_hists[proc + syst].Fill(1, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 1, ">3j 2t", syst, weight)

        if vd["numJets"][0] < 4 and vd["numBTagM"][0] ==2:
            jet_count_hists[proc + syst].GetXaxis().SetBinLabel( 1, ">3j 2t")
            jet_count_hists[proc + syst].Fill(0, weight)
            if proc[:6] == "TTJets":
                fill_ttjets_histograms_singlevar(vd, jet_count_hists, 0, "<4j 2t", syst, weight)
                                        
