import ROOT, sys
from array import array
import numpy as np

lepton_vars_f = ["lepton_pt", "lepton_eta", "lepton_rIso", "lepton_charge"]
jet_vars_f = ["jet_pt", "jet_eta", "btag_LR", "jet_csv"]

#----------------separate by type---------------------
int_list = ["nLep", "numJets", "numBTagL", "numBTagM", "numBTagT", "nPVs"]
int_array_list = ["lepton_type"]
float_list = ["weight", "trigger", "PUweight", "MET_pt", "MET_phi"] 
float_array_list = lepton_vars_f  + jet_vars_f #lepton_vars_d + jet_vars_d
trigger = ["triggerFlags"]

var_list = int_list + int_array_list + float_list + float_array_list + trigger
#-------------------------------------------

def var_type(var_name):
    """
    return the variable type for tree entry
    """
    maxpart = 20
    if var_name in int_list: return array('i',[0])
    if var_name in int_array_list: return array('i',[0]*maxpart)

    if var_name in float_list: return array('f', [0])
    if var_name in float_array_list: return array('f', [0]*maxpart)
    if var_name in trigger: return array('b', [0]*70)

#    if var_name in int_2D_array_list: return np.array( np.zeros( (maxpart, maxhit) ), dtype=np.int32) 
#    if var_name in float_2D_array_list: return np.array( np.zeros( (maxpart, maxhit) ), dtype=np.float32 ) 



def initialize_tree(tree, var_list):
    vt = dict([ (v, var_type(v)) for v in var_list ]) #associate proper data type for variables in the tree
    tree.SetBranchStatus("*",0)
    for v in var_list:
        tree.SetBranchStatus(v, 1)
        tree.SetBranchAddress(v, vt[v])
        tree.AddBranchToCache(v, ROOT.kTRUE)

    tree.StopCacheLearningPhase()
    return vt
    

def pass_trigger_selection(  vd, mode, dataset ):
    """
    dataset = "el", "mu"
    """
    pass_trigger_sel = False

    if mode=="SL":
        if dataset == "mu" and ( vd["triggerFlags"][22]>0 or vd["triggerFlags"][23]>0 or vd["triggerFlags"][14]>0 or vd["triggerFlags"][21]>0): 
            pass_trigger_sel = True
        elif dataset == "el" and ( vd["triggerFlags"][3]>0 or vd["triggerFlags"][44]>0 ):
            pass_trigger_sel = True

    elif mode=="DL":
        if dataset == "el" and ( vd["triggerFlags"][5] > 0 or vd["triggerFlags"][6] > 0 ) : 
            pass_trigger_sel = True
        elif dataset == "mu" and (vd["triggerFlags"][2] > 0 or vd["triggerFlags"][3] > 0 ):
            pass_trigger_sel = True


    return pass_trigger_sel

def pass_lepton_selection( vd, mode ):
    """
    vd = dictionary of event variables
    mode = "SL" or "DL"
    max 2 leptons saved in event, take care if not the case!
    check lepton selection
    """
    passlist = []
    pass_lep_sel = False
    n_lep = vd['nLep'][0]
    
        
    if mode == "SL":
        for ilep in range(n_lep):
            lep_eta = abs(vd["lepton_eta"][ilep])
            lep_pt = vd["lepton_pt"][ilep]
            
            if (  lep_pt > 30 and vd["lepton_rIso"][ilep] < 0.1 ):
                if abs( vd["lepton_type"][ilep] == 13 and lep_eta < 2.1 ): # if muon
                    passlist.append(ilep)
                elif abs( vd["lepton_type"][ilep] == 11 and lep_eta < 2.5 and (lep_eta > 1.566 or lep_eta < 1.442)): 
                    passlist.append(ilep)

        if len(passlist) == 1:
            pass_lep_sel = True

    if mode == "DL" and n_lep > 1:
#        lep_eta_1 = abs(vd["lepton_eta"][0])
#        lep_eta_2 = abs(vd["lepton_eta"][1])
#        lep_pt_1 = vd["lepton_pt"][0]
#        lep_pt_2 = vd["lepton_pt"][1]
                   
        for ilep in range(n_lep):
            lep_eta = abs(vd["lepton_eta"][ilep])
            lep_pt = vd["lepton_pt"][ilep]
            lep_iso = vd["lepton_rIso"][ilep]

            if( lep_pt > 10 and lep_iso < 0.2): # loose requirement
                if abs( vd["lepton_type"][ilep] == 13 and lep_eta < 2.3 ): # if muon 
                    passlist.append(ilep)
                if abs( vd["lepton_type"][ilep] == 11 and lep_eta < 2.5 and (lep_eta < 1.442 or lep_eta > 1.566) ): # if electron
                    passlist.append(ilep)

        if len(passlist) == 2 and vd["lepton_charge"][passlist[0]]*vd["lepton_charge"][passlist[1]] < 0:
            if vd["lepton_pt"][0] > 20 and vd["lepton_rIso"][0] < 0.1:
                pass_lep_sel = True
            elif vd["lepton_pt"][1] > 20 and vd["lepton_rIso"][1] < 0.1:
                passlist = passlist[::-1] #reverse order
                pass_lep_sel = True
            
    if pass_lep_sel:
        return passlist
    
    else:
        return []

def pass_jet_selection(vd, mode ):
    passlist_tight = []
    passlist_loose = []

    n_jet = vd["numJets"][0]

    for ijet in range(n_jet):
        jet_pt = vd["jet_pt"][ijet]
        jet_eta = abs(vd["jet_eta"][ijet])

        if( jet_pt > 40 and jet_eta < 2.5):
            passlist_tight.append(ijet)
        
        elif( jet_pt > 30 ):
            passlist_loose.append(ijet)

#    if mode == "SL" and len(passlist_tight) > 3 and len(passlist_tight) + len(passlist_loose) > 4 and len(passlist_tight) + len(passlist_loose) < 8:
    if mode == "SL" and len(passlist_tight) > 3:
       return passlist_tight #+ passlist_loose
#    elif mode== "DL" and len(passlist_tight) > 2 and len(passlist_tight) + len(passlist_loose) > 3 and len(passlist_tight) + len(passlist_loose) < 5:
    if mode == "DL" and len(passlist_tight) > 3:
        return passlist_tight #+ passlist_loose
        

    else:
        return []

    

