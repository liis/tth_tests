import ROOT, sys

hist_variables = {"MET_pt": (50, 0 , 250),
                  "MET_phi": (50, -3.15, 3.15),
                  "lepton_pt":(50, 0, 250),

                  "electron_eta":(50, -2.5, 2.5),
                  "electron_pt": (50, 0, 250),
                  "electron_rIso": (50, 0, 0.15),

                  "muon_rIso": (50, 0, 0.15),
                  "muon_pt": (50, 0, 250),
                  "muon_eta":(50, -2.5, 2.5),

                  "jet_pt": (50, 0, 250),
                  "numJets": (8, 3, 11),

                  "numBTagM": (8, 0, 8),
                  "numBTagL":(8, 0, 8),
                  "numBTagT": (8, 0, 8),

                  "btag_LR": (50, 0, 1),
                  
                  "nPVs": (50, 0, 50)

                  }

variable_names = {"MET_pt": "MET",
                  "MET_phi": "MET #phi",
                  "lepton_pt": "lepton p_{T}",

                  "electron_eta": "Electron #eta",
                  "electron_rIso": "Electron isolation",
                  "electron_pt": "Electron p_{T}",

                  "muon_pt": "Muon p_{T}",
                  "muon_rIso": "Muon isolation",
                  "muon_eta": "Muon #eta",
                  
                  "lepton_rIso": "Lepton isolation",
                  "lepton_type": "Lepton type",
                  "jet_pt": "jet p_{T}",

                  "numJets": "Number of jets",
                  "numBTagM": "Number of b-tagged jets (Medium)",
                  "numBTagL": "Number of b-tagged jets (Loose)",
                  "numBTagT": "Number of b-tagged jets (Tight)",

                  "nPVs": " # primary vertices",

                  "btag_LR": "b-tagging LR"

                  }

colors = {"TTJets": ROOT.kRed,
          "EWK": ROOT.kYellow+1,
          "DiBoson": ROOT.kBlue,
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
        histos[variable] = h

    return histos

def write_histograms_to_file(outfilename, hists):
    p = ROOT.TFile(outfilename,"recreate")
    
    for sample in hists:
        dir = p.mkdir(sample)
        for variable in hists[sample]:
            dir.cd()
            hists[sample][variable].Write()

    p.Close()
