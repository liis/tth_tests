import ROOT, sys, re

hist_variables = {
    "MET_pt": (50, 0 , 250),
    "MET_phi": (50, -3.15, 3.15),

    "lead_electron_eta":(50, -2.5, 2.5),
    "lead_electron_pt": (50, 0, 250),
    "lead_electron_rIso": (50, 0, 0.15),

    "trail_electron_eta":(25, -2.5, 2.5),
    "trail_electron_pt": (25, 0, 250),
    "trail_electron_rIso": (50, 0, 0.25),
    "trail_electron_wp95": (2,0,2),
    "trail_electron_wp80": (2,0,2),
    "trail_electron_dxy": (25, 0, 0.05),
    "trail_electron_dz": (100, 0, 1.1),

    "lead_muon_rIso": (50, 0, 0.15),
    "lead_muon_pt": (50, 0, 250),
    "lead_muon_eta":(50, -2.5, 2.5),

    "trail_muon_rIso": (50, 0, 0.25),
    "trail_muon_pt": (25, 0, 250),
    "trail_muon_eta":(25, -2.5, 2.5),

    "lead_jet_pt": (50, 0, 500),
    "lead_jet_eta": (50, -3, 3),
    "lead_jet_phi": (50, -3.15, 3.15),

    "numJets": (12, 0, 12),
    
    "numBTagM": (8, 0, 8),
    
    "numBTagL":(8, 0, 8),
    "numBTagT": (8, 0, 8),

    "nPVs": (50, 0, 50),

    "btag_LR_4j": ( 50, 0, 1),
    "btag_LR_5j": ( 50, 0, 1),
    "btag_LR_6j": ( 50, 0, 1),
    "btag_LR_7j": ( 50, 0, 1),    

    #----- count hists -----------
#    "cut_flow": (35, 0, 35),
    "jet_count": (7, 0 , 7),
    "btag_count": (4, 0, 4),
    "category_count": (4, 0, 4)

    }

def initialize_hist_ranges( mode, hist_variables = hist_variables):
    if mode == "DL":
        hist_variables["jet_count"] = (4, 0, 4)
        hist_variables["category_count"] = (3, 0, 3)
        hist_variables["btag_LR_4j"] = (25, 0, 1)

        hist_variables["lead_electron_eta"] = (25, -2.5, 2.5)
        hist_variables["lead_electron_pt"] = (25, 0, 250)
        hist_variables["lead_muon_eta"] = (25, -2.5, 2.5)
        hist_variables["lead_muon_pt"] = (25, 0, 250)
            
    return hist_variables


map_hist_variables = { # if histogram name is different from the tree entry name

    "lead_electron_pt": "lepton_pt",
    "lead_electron_eta": "lepton_eta",
    "lead_electron_rIso": "lepton_rIso",

    "trail_electron_pt": "lepton_pt",
    "trail_electron_rIso": "lepton_rIso",   
    "trail_electron_eta": "lepton_eta",
    "trail_electron_wp80": "lepton_wp80",
    "trail_electron_wp95": "lepton_wp95",
    "trail_electron_dxy": "lepton_dxy",
    "trail_electron_dz": "lepton_dz",

    "lead_muon_pt": "lepton_pt",
    "lead_muon_eta": "lepton_eta",
    "lead_muon_rIso": "lepton_rIso",

    "trail_muon_pt": "lepton_pt",
    "trail_muon_eta": "lepton_eta",
    "trail_muon_rIso": "lepton_rIso",

    "lead_jet_pt": "jet_pt",
    "lead_jet_eta": "jet_eta",
    "lead_jet_phi": "jet_phi",

#    "numBTagM_sel": "numBTagM",
#    "numJets_sel": "numJets",

    "btag_lr_7j": "btag_LR",
    "btag_lr_6j": "btag_LR",
    "btag_lr_5j": "btag_LR",
    "btag_lr_4j": "btag_LR",
    }

variable_names = {
    "MET_pt": "MET",
    "MET_phi": "MET #phi",
#                  "lepton_pt": "lepton p_{T}",
    
    "lead_electron_eta": "Electron #eta",
    "lead_electron_rIso": "Electron isolation",
    "lead_electron_pt": "Electron p_{T}",
    
    #                "trail_electron_eta": "Electron #eta",
    #                "trail_electron_rIso": "Electron isolation",
    #                "trail_electron_pt": "Electron p_{T}",
    
    "lead_muon_pt": "Muon p_{T}",
    "lead_muon_rIso": "Muon isolation",
    "lead_muon_eta": "Muon #eta",
    
    #               "trail_muon_pt": "Muon p_{T}",
   #               "trail_muon_rIso": "Muon isolation",
    #               "trail_muon_eta": "Muon #eta",
    
    #                  "jet_pt": "jet p_{T}",
    #                  "jet_eta": "jet #eta",
    #                  "jet_phi": "jet #phi",
    
    "lead_jet_pt": "leading jet p_{T}",
    "lead_jet_eta": "leading jet #eta",
    "lead_jet_phi": "leading jet #phi",
    
    "numJets": "Number of jets",
    #              "numJets_sel": "Number of sel. jets",
    
    "numBTagM": "Number of b-tagged jets (Medium)",
    #             "numBTagM_sel": "Number of sel. b-tagged jets (Medium)",
    
    "numBTagL": "Number of b-tagged jets (Loose)",
    "numBTagT": "Number of b-tagged jets (Tight)",
    
    "nPVs": " # primary vertices",
    
    #           "btag_LR": "b-tagging LR",
    "btag_lr_7j": "b-tagging LR (>= 7 jets)",
    "btag_lr_6j": "b-tagging LR (6 jets)",
    "btag_lr_5j": "b-tagging LR (5 jets)" ,
    "btag_lr_4j": "b-tagging LR (4 jets)",

    "jet_count": "Nr. of jets",
    "btag_count": "Nr. of b-tags (CSV medium)",
    "cat_count": "Selection categories",
    }

colors = {"TTJets": ROOT.kBlue,
          "ttbb": 16,
          "ttb": 17,
          "ttjj": 18,
          "EWK": ROOT.kGreen+3,
          "DiBoson": ROOT.kYellow+1,
          "TTH125": ROOT.kRed,
          "TTV": 30,
          "SingleTop": ROOT.kMagenta
          }



def initialize_histograms( sample, hist_variables, syst = ""):
    """
    sample - sample name
    var_list - dictionary of variable names and hist parameters
    """
    histos = {}
    for variable, reg in hist_variables.iteritems():
        histname = variable + "_" + sample + syst
        h = ROOT.TH1F(histname, histname, reg[0], reg[1], reg[2])
        h.Sumw2() # errors
        histos[variable] = h

    return histos

def write_histograms_to_file(outfilename, hists, additional_hist_per_sample = [], additional_hists = []):
    """
    hists -- dict of histograms per sample and variable
    cut_flow -- dict of cutflow hists per sample
    additional_hists -- separate histograms for parameters
    """
    p = ROOT.TFile(outfilename,"recreate")

    print "saving cut-flow histograms"
    for hist in additional_hists:
        hist.Write()
    
    for sample in hists:
        dir = p.mkdir(sample)
        dir.cd()
        for hist in additional_hist_per_sample:
#            print "opening " + str(hist[sample])
            hist[sample].Write()
            
        for variable in hists[sample]:
            hists[sample][variable].Write()

    p.Close()

def fill_ttjets_histograms( vd, hists, varname, var, syst, weight ):
    """
    Apply gen level filter to separate subprocesses of ttjj. Seva histograms separately
    """
    if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
        hists["ttbb" + syst][varname].Fill(var, weight)

    elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
        hists["ttb" + syst][varname].Fill(var, weight)

    elif vd["nSimBs"][0] == 2:
        hists["ttjj" + syst][varname].Fill(var, weight)

def fill_single_histogram(vd, varname, var, hists, sample, syst, weight):
    hists[sample + syst][varname].Fill(var, weight)
    if sample == "TTJets":
        fill_ttjets_histograms( vd, hists, varname, var, syst, weight)
    
def fill_1D_histograms( vd, hists, sample, syst, weight, mode, isTTjets = False): #FIXME!! this is bad implementation
    
    for var in hists[sample]: # loop over dictionary of histograms for a specific datasample
        try:
            var_tree = var
            var_size = len(vd[var])
        except KeyError:
            var_tree = map_hist_variables[var]
            var_size = len(vd[var_tree])
            
        if var_size == 1:
            hists[sample+syst][var].Fill(vd[var_tree][0], weight)
            if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[var_tree][0], syst, weight) 


def fill_lepton_histograms(vd, hists, sample, syst, weight, mode, lepton_list = [], isTTjets = False):

    if len(lepton_list) == 0: # if not specified, consider all leptons
        lepton_list = range(vd["nLep"][0])

    for var in hists[sample]: # loop over dictionary of histograms for a specific datasample
        if (  re.search("electron",var) and vd["lepton_type"][0] == 11 ) or (  re.search("muon",var) and vd["lepton_type"][0] == 13 ): 
            
            if re.search("lead", var): # fill histograms for leading leptons
                hists[sample+syst][var].Fill(vd[ map_hist_variables[var] ][ lepton_list[0] ], weight)
                if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[ map_hist_variables[var] ][ lepton_list[0] ], syst, weight)

            elif mode == "DL" and re.search("trail", var): # fill histograms for trailing leptons
                hists[sample+syst][var].Fill(vd[ map_hist_variables[var] ][ lepton_list[1] ], weight)
                if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[ map_hist_variables[var] ][ lepton_list[1] ], syst, weight)


def fill_jet_histograms(vd, hists, sample, syst, weight, mode, jet_list = [], isTTjets = False):
    
    if len(jet_list) == 0:
        jet_list = range(vd["numJets"][0])

    hists[sample + syst]["numJets"].Fill( vd["numJets"][0], weight )
    if isTTjets: fill_ttjets_histograms(vd, hists, "numJets", vd["numJets"][0], syst, weight)
    
#    hists[sample]["numJets_sel"].Fill( len(jet_list), weight )
#    if isTTjets: fill_ttjets_histograms(vd, hists, "numJets_sel", len(jet_list), weight)

    for var in hists[sample]:
        if re.search("lead_jet", var):
            var_tree = map_hist_variables[var]
            hists[sample + syst][var].Fill( vd[var_tree][2], weight) # pick leading jet after lepton [0] and MET [1]
            if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[var_tree][2], syst, weight)

          #  elif( re.search("jet_", var) ):
          #      for ijet in jet_list:
          #          hists[sample][var].Fill( vd[var][ijet], weight)
          #          if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[var][ijet], weight)

    
def fill_cut_flow(cuts, cf_hist, lf = 1, tablewidth = 0, bf = False, round_prec = 1):
    """
    cuts -- ordered dictionary of cuts in cut-flow. labels need to be saved in the cut-flow histogra
    cf_hist -- cut-flow histogram
    lf -- optional scale factor for the yields
    """
    if tablewidth == 0:
        tablewidth = len(cuts)
    cut_count = 0
    for cut in cuts:
        cut_count += 1
#        round_prec = 1 # rounding precision when printing
        
        cf_hist.Scale(lf) # optionally normalize to different lumi value

        bin_nr = cf_hist.GetXaxis().FindBin(cut) # find bin by cut-label
        nr_evts = cf_hist.GetBinContent(bin_nr)
        print " & ",

        if not bf:
            print str( round( nr_evts, round_prec) ) + " $\pm$ " + str( round( cf_hist.GetBinError(bin_nr), round_prec ) ),
        else:
            print "\\textbf{" + str( round( nr_evts, round_prec) ) + " $\pm$ " + str( round( cf_hist.GetBinError(bin_nr), round_prec ) ) + "}",

def set_file_name(file_name_base, mctrig, topw, noWeight, dosys=False):
    infile = file_name_base
    if not mctrig:
        infile = infile + "_notrig"
    if not topw:
        infile = infile + "_notopw"
    if dosys:
        infile = infile + "_withSys"
    if noWeight:
        infile = infile + "_noWeight"

    infile = infile + ".root"
    return infile

def get_ratio(hist1, hist2, ratio_ytitle = ""):
    """
    hist1 -- numerator
    hist2 -- denominator
    """
    hist_ratio = hist1.Clone()
    hist_ratio.Divide(hist2)

    hist_ratio.SetStats(False)
    hist_ratio.SetMarkerStyle(20)
    hist_ratio.SetMarkerSize(0.35)
    hist_ratio.SetMarkerColor(ROOT.kBlack)
    hist_ratio.SetLineColor(ROOT.kBlack)
    hist_ratio.SetMaximum(2)
    hist_ratio.SetMinimum(0.)
    
    xAxis = hist_ratio.GetXaxis()
    yAxis = hist_ratio.GetYaxis()

    yAxis.CenterTitle()
    yAxis.SetTitle(ratio_ytitle)
    yAxis.SetTitleOffset(0.2)
    yAxis.SetTitleSize(0.18)
    yAxis.SetLabelSize(0.15)
    yAxis.SetNdivisions(3)
    
    xAxis.SetLabelSize(0.01)
    xAxis.SetTitleSize(0.15)
    xAxis.SetTitleOffset(0.5)
    xAxis.SetTitle("")
                                                                             
    return hist_ratio
                                    
def event_count(ncut, binlabel, cut_flow_hists, proc, weight, vd, idx_sys = 0):
    """
    idx_sys -- only fill nominal FIXME
    """
    if idx_sys == 0: #FIXME
        cut_flow_hists[proc].GetXaxis().SetBinLabel(ncut+1, binlabel)
        cut_flow_hists[proc].Fill(ncut,weight)
        
        if proc == "TTJets":
            if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
                cut_flow_hists["ttbb"].GetXaxis().SetBinLabel(ncut+1, binlabel)
                cut_flow_hists["ttbb"].Fill(ncut, weight)
            elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
                cut_flow_hists["ttb"].GetXaxis().SetBinLabel(ncut+1, binlabel)
                cut_flow_hists["ttb"].Fill(ncut, weight)
            elif vd["nSimBs"][0] == 2:
                cut_flow_hists["ttjj"].GetXaxis().SetBinLabel(ncut+1, binlabel)
                cut_flow_hists["ttjj"].Fill(ncut, weight)

    
