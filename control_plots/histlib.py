import ROOT, sys, re

hist_variables = {
    "MET_pt": (50, 0 , 250),
    "MET_phi": (50, -3.15, 3.15),
        
    "lead_electron_eta":(50, -2.5, 2.5),
    "lead_electron_pt": (50, 0, 250),
    "lead_electron_rIso": (50, 0, 0.15),

    "trail_electron_eta":(50, -2.5, 2.5),
    "trail_electron_pt": (50, 0, 250),
    "trail_electron_rIso": (50, 0, 0.15),

    "lead_muon_rIso": (50, 0, 0.15),
    "lead_muon_pt": (50, 0, 250),
    "lead_muon_eta":(50, -2.5, 2.5),

    "trail_muon_rIso": (50, 0, 0.15),
    "trail_muon_pt": (50, 0, 250),
    "trail_muon_eta":(50, -2.5, 2.5),

    "lead_jet_pt": (50, 0, 250),
    "lead_jet_eta": (50, -3, 3),
    "lead_jet_phi": (50, -3.15, 3.15),

    "jet_pt": (50, 0, 250),
    "jet_eta": (200, -3, 3),
    "jet_phi": (50, -3.15, 3.15),

    "numJets": (12, 0, 12),
    "numJets_sel":(12, 0, 12),
    
    "numBTagM": (8, 0, 8),
    "numBTagM_sel":(8,0,8),
    
    "numBTagL":(8, 0, 8),
    "numBTagT": (8, 0, 8),

    "btag_LR": (50, 0, 1),
    
    "nPVs": (50, 0, 50)
    
    }

map_hist_variables = { # if histogram name is different from the tree entry name

    "lead_electron_pt": "lepton_pt",
    "lead_electron_eta": "lepton_eta",
    "lead_electron_rIso": "lepton_rIso",

    "trail_electron_pt": "lepton_pt",
    "trail_electron_rIso": "lepton_rIso",   
    "trail_electron_eta": "lepton_eta",

    "lead_muon_pt": "lepton_pt",
    "lead_muon_eta": "lepton_eta",
    "lead_muon_rIso": "lepton_rIso",

    "trail_muon_pt": "lepton_pt",
    "trail_muon_eta": "lepton_eta",
    "trail_muon_rIso": "lepton_rIso",

    "lead_jet_pt": "jet_pt",
    "lead_jet_eta": "jet_eta",
    "lead_jet_phi": "jet_phi",

    "numBTagM_sel": "numBTagM",
    "numJets_sel": "numJets"
    }

variable_names = {"MET_pt": "MET",
                  "MET_phi": "MET #phi",
                  "lepton_pt": "lepton p_{T}",

                  "lead_electron_eta": "Electron #eta",
                  "lead_electron_rIso": "Electron isolation",
                  "lead_electron_pt": "Electron p_{T}",

                  "trail_electron_eta": "Electron #eta",
                  "trail_electron_rIso": "Electron isolation",
                  "trail_electron_pt": "Electron p_{T}",

                  "lead_muon_pt": "Muon p_{T}",
                  "lead_muon_rIso": "Muon isolation",
                  "lead_muon_eta": "Muon #eta",

                  "trail_muon_pt": "Muon p_{T}",
                  "trail_muon_rIso": "Muon isolation",
                  "trail_muon_eta": "Muon #eta",
                  
                  "lepton_rIso": "Lepton isolation",
                  "lepton_type": "Lepton type",
                 
                  "jet_pt": "jet p_{T}",
                  "jet_eta": "jet #eta",
                  "jet_phi": "jet #phi",

                  "lead_jet_pt": "leading jet p_{T}",
                  "lead_jet_eta": "leading jet #eta",
                  "lead_jet_phi": "leading jet #phi",

                  "numJets": "Number of jets",
                  "numJets_sel": "Number of sel. jets",

                  "numBTagM": "Number of b-tagged jets (Medium)",
                  "numBTagM_sel": "Number of sel. b-tagged jets (Medium)",

                  "numBTagL": "Number of b-tagged jets (Loose)",
                  "numBTagT": "Number of b-tagged jets (Tight)",

                  "nPVs": " # primary vertices",

                  "btag_LR": "b-tagging LR"

                  }

colors = {"TTJets": ROOT.kBlue,
          "ttbb": ROOT.kBlue - 8,
          "ttb": ROOT.kBlue - 5,
          "ttjj": ROOT.kBlue + 3,
          "EWK": ROOT.kYellow+1,
          "DiBoson": ROOT.kRed,
          "TTH125": ROOT.kWhite,
          "TTV": ROOT.kGreen + 3,
          "SingleTop": ROOT.kViolet
          }



def initialize_histograms( sample, hist_variables):
    """
    sample - sample name
    var_list - dictionary of variable names and hist parameters
    """
    histos = {}
    for variable, reg in hist_variables.iteritems():
        histname = variable + "_" + sample
        h = ROOT.TH1F(histname, histname, reg[0], reg[1], reg[2])
        h.Sumw2() # errors
        histos[variable] = h

    return histos

def write_histograms_to_file(outfilename, hists, cut_flow):
    p = ROOT.TFile(outfilename,"recreate")
    
    for sample in hists:
        dir = p.mkdir(sample)
        dir.cd()
        cut_flow[sample].Write()
        for variable in hists[sample]:
            hists[sample][variable].Write()

    p.Close()

def fill_ttjets_histograms( vd, hists, varname, var, weight ):
    """
    Apply gen level filter to separate subprocesses of ttjj. Seva histograms separately
    """
    if vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] > 1:
        hists["ttbb"][varname].Fill(var, weight)

    elif vd["nSimBs"][0] > 2 and vd["nMatchSimBs"][0] < 2:
        hists["ttb"][varname].Fill(var, weight)

    elif vd["nSimBs"][0] == 2:
        hists["ttjj"][varname].Fill(var, weight)


def fill_1D_histograms( vd, hists, sample, weight, mode, isTTjets = False):
    
    for var in hists[sample]: # loop over dictionary of histograms for a specific datasample
        try:
            var_tree = var
            var_size = len(vd[var])
        except KeyError:
            var_tree = map_hist_variables[var]
            var_size = len(vd[var_tree])
            
        if var_size == 1:
            hists[sample][var].Fill(vd[var_tree][0], weight)
            if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[var_tree][0], weight) 


def fill_lepton_histograms(vd, hists, sample, weight, mode, lepton_list = [], isTTjets = False):

    if len(lepton_list) == 0: # if not specified, consider all leptons
        lepton_list = range(vd["nLep"][0])

    for var in hists[sample]: # loop over dictionary of histograms for a specific datasample
        if (  re.search("electron",var) and vd["lepton_type"][0] == 11 ) or (  re.search("muon",var) and vd["lepton_type"][0] == 13 ): 
            
            if re.search("lead", var): # fill histograms for leading leptons
                hists[sample][var].Fill(vd[ map_hist_variables[var] ][ lepton_list[0] ], weight)
                if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[ map_hist_variables[var] ][ lepton_list[0] ], weight)

            elif mode == "DL" and re.search("trail", var): # fill histograms for trailing leptons
                hists[sample][var].Fill(vd[ map_hist_variables[var] ][ lepton_list[1] ], weight)
                if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[ map_hist_variables[var] ][ lepton_list[1] ], weight)


def fill_jet_histograms(vd, hists, sample, weight, mode, jet_list = [], isTTjets = False):
    
    if len(jet_list) == 0:
        jet_list = range(vd["numJets"][0])

    hists[sample]["numJets"].Fill( vd["numJets"][0], weight )
    if isTTjets: fill_ttjets_histograms(vd, hists, "numJets", vd["numJets"][0], weight)
    
    hists[sample]["numJets_sel"].Fill( len(jet_list), weight )
    if isTTjets: fill_ttjets_histograms(vd, hists, "numJets_sel", len(jet_list), weight)

    for var in hists[sample]:
        if re.search("lead_jet", var):
            var_tree = map_hist_variables[var]
            hists[sample][var].Fill( vd[var_tree][2], weight) # pick leading jet after lepton [0] and MET [1]
            if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[var_tree][2], weight)

          #  elif( re.search("jet_", var) ):
          #      for ijet in jet_list:
          #          hists[sample][var].Fill( vd[var][ijet], weight)
          #          if isTTjets: fill_ttjets_histograms(vd, hists, var, vd[var][ijet], weight)

    
def fill_cut_flow(cuts, cf_hist):
    """
    cuts -- ordered dictionary of cuts in cut-flow. labels need to be saved in the cut-flow histogra
    cf_hist -- cut-flow histogram
    """
    cut_count = 0
    for cut in cuts:
        cut_count += 1

        bin_nr = cf_hist.GetXaxis().FindBin(cut) # find bin by cut-label
        nr_evts = cf_hist.GetBinContent(bin_nr)
        print str( round( nr_evts, 1) ) + " $\pm$ " + str( round( cf_hist.GetBinError(bin_nr), 1 ) ),
        
        if cut_count < len(cuts):
            print " & ",
        else:
            print "\\\\"
