import ROOT, sys

input_files = {
    "ttH125": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTH125.root",
    "TTJets":"MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTJets.root",
    "TTV": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_TTV.root",
    "SingleT": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_SingleT.root",
    "DiBoson": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_DiBoson.root",
    "EWK": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_EWK.root",
    "diMu_data": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_Run2012_SingleMu.root",
    "diEl_data": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_Run2012_DoubleElectron.root",
    "singleMu_data": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_Run2012_SingleMu.root",
    "singleEl_data": "MEAnalysisNew_all_ntuplizeAll_v3_rec_std_Run2012_SingleElectron.root"
    }

input_files_pre_Apr14 = {
    "ttH125": "MEAnalysisNew_nominal_0-0-1_rec_std_TTH125.root",
    "TTJets":"MEAnalysisNew_nominal_0-0-1_rec_std_TTJets.root",
    "TTV": "MEAnalysisNew_nominal_0-0-1_rec_std_TTV.root",
    "SingleT": "MEAnalysisNew_nominal_0-0-1_rec_std_SingleT.root",
    "DiBoson": "MEAnalysisNew_nominal_0-0-1_rec_std_DiBoson.root",
    "EWK": "MEAnalysisNew_nominal_0-0-1_rec_std_EWK.root",
    "diMu_data": "MEAnalysisNew_nominal_0-0-1_v3_rec_std_Data_SingleMu.root", 
    "diEl_data": "MEAnalysisNew_nominal_0-0-1_rec_std_Data_DoubleElectron.root",
    "singleMu_data": "MEAnalysisNew_nominal_0-0-1_rec_std_Data_SingleMu.root",
    "singleEl_data": "MEAnalysisNew_nominal_0-0-1_rec_std_Data_SingleElectron.root"
    }

input_files = input_files
