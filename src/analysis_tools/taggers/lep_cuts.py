# Defining all the boolean masks I use for my object cuts
#The general key is obj == ele, lpte, or muon. 
#if a given mask (function) is for a specific obj type, it's in the definition of said function
#example: ele_gen_mask(ele)

#import sys
#path_to_tools = '/home/cms-jovyan/dwg_analysis_v3/tools/'
#sys.path.insert(1, path_to_tools)

import awkward as ak
import numpy as np
import hist.dask as dah
from coffea.analysis_tools import PackedSelection
from coffea.nanoevents import NanoAODSchema


from .gen_filter import *
from .vid_unpacked import *

###########################################################################
# Sim-only masks (all imported from gen_filter.py)

def gflav0(obj): return gflav0_mask(obj)
def gflav1(obj): return gflav1_mask(obj)
def gflav4(obj): return gflav4_mask(obj)
def gflav5(obj): return gflav5_mask(obj)
def gflav15(obj): return gflav15_mask(obj)
def heavy_decay(obj): return heavy_decay_mask(obj)

def susy_mask(obj): return susy_mask(obj)
def WZ_mask(obj): return WZ_mask(obj)
def gen_parent(obj): return parent_mask(obj)
    
def ele_gen(ele): return ele_gen_mask(ele)
def lpte_gen(lpte): return lpte_gen_mask(lpte)
def muon_gen(muon): return muon_gen_mask(muon)

def conv_veto(lpte): return lpte.convVeto == 1

# Define filtered masks

def primary_mask(obj): return (gflav1(obj) & gen_parent(obj))
    
def light_fake_mask(obj): return gflav0(obj)

def heavy_fake_mask(obj): return heavy_decay(obj)

###########################################################################
# general masks for ele, lpte, muon

def pt_selection(obj, pt_min=0, pt_max=np.inf): return (pt_min <= obj.pt) & (obj.pt < pt_max)

def eta_2p5(obj): return (np.abs(obj.eta) < 2.5)

def loose_sip3d(obj): return (obj.sip3d < 8)
def tight_sip3d(obj): return (obj.sip3d < 2)

def dxy_0p05(obj): return (np.abs(obj.dxy) < 0.05)
def dz_0p1(obj): return (np.abs(obj.dz) < 0.1)

#pfRelIso only exists for regular electrons and muons
def loose_pfRelIso(obj): return (obj.pfRelIso03_all * obj.pt) < (20 + (300/obj.pt))
def tight_pfRelIso(obj): return (obj.pfRelIso03_all * obj.pt) <= 4

def loose_miniRelIso(obj): return (obj.miniPFRelIso_all * obj.pt) < (20 + (300/obj.pt))
def tight_miniRelIso(obj): return (obj.miniPFRelIso_all * obj.pt) <= 4

def pfRelIso(obj, tight=True):
    return tight_pfRelIso(obj) if tight else loose_pfRelIso(obj)

def miniIso(obj, tight=True):
    return tight_miniRelIso(obj) if tight else loose_miniRelIso(obj)


###########################################################################
# LowPtElectron masks only:

def loose_ID(lpte): return lpte.ID >= 1
def loose_ID_new(lpte): return lpte.ID >= 1.5
def tight_ID(lpte): return lpte.ID >= 2.2
def tighter_ID(lpte): return lpte.ID >= 2.5

def loose_sip3d_lpte(lpte): return (lpte_sip3d(lpte) < 8)
def tight_sip3d_lpte(lpte): return (lpte_sip3d(lpte) < 2)

# pt > 5 ID in eta regions
def pt_5_8_outter_eta(lpte):
    return (lpte.pt >= 5) & (np.abs(lpte.eta) >= 1.48) & (np.abs(lpte.eta) < 2.5) & (lpte.ID >= 3.5)

def pt_5_8_middle_eta(lpte):
    return (lpte.pt >= 5) & (np.abs(lpte.eta) >= 0.8) & (np.abs(lpte.eta) < 1.48) & (lpte.ID >= 3)

def pt_5_8_central_eta(lpte):
    return (lpte.pt >= 5) & (np.abs(lpte.eta) < 0.8) & (lpte.ID >= 2.3)

def pt_5_8_eta_ID(lpte):
    return pt_5_8_outter_eta(lpte) | pt_5_8_middle_eta(lpte) | pt_5_8_central_eta(lpte)

# pt < 5 ID in eta regions

def pt_2_5_middle_eta(lpte):
    return (lpte.pt < 5) & (np.abs(lpte.eta) >= 0.8) & (np.abs(lpte.eta) < 1.48) & (lpte.ID >= 3)

def pt_2_5_central_eta(lpte):
    return (lpte.pt < 5) & (np.abs(lpte.eta) < 0.8) & (lpte.ID >= 2.3)

def pt_2_5_eta_ID(lpte):
    return pt_2_5_middle_eta(lpte) | pt_2_5_central_eta(lpte)


def central_eta_ID_regions(lpte):
    return pt_5_8_eta_ID(lpte) | pt_2_5_eta_ID(lpte)

###########################################################################
# Modified ID (for Regular Electron collection only) imported from vid_unpacked.py

def tight_no_iso(ele): return tight_minus_iso(ele)
def veto_no_iso(ele): return veto_minus_iso(ele)

def veto_no_hoe(ele): return veto_minus_hoe(ele)
def tight_no_hoe(ele): return tight_minus_hoe(ele)
    
def veto_no_iso_hoe(ele): return veto_minus_iso_hoe(ele)
def tight_no_iso_hoe(ele): return tight_minus_iso_hoe(ele)

def tightCharge_1(ele): return (ele.tightCharge == 1)
def tightCharge_2(ele): return (ele.tightCharge == 2)

    
#(0:fail, 1:veto, 2:loose, 3:medium, 4:tight)
def cutbased_VETO(ele): return (ele.cutBased == 1)
def cutbased_LOOSE(ele): return (ele.cutBased == 2)
def cutbased_MEDIUM(ele): return (ele.cutBased == 3)
def cutbased_TIGHT(ele): return (ele.cutBased == 4)

def mvaIso_WP80(ele): return (ele.mvaIso_WP80)
def mvaIso_WP90(ele): return (ele.mvaIso_WP90)


###########################################################################
# Muon IDs

def muon_looseID(muon): return muon.looseId
def muon_mediumID(muon): return muon.mediumId
def muon_tightID(muon): return muon.tightId
def muon_softID(muon): return muon.softId
def muon_softMvaID(muon): return muon.softMvaId




""
def lpte_sip3d(lpte):
     
    #approximation or rough calculation based on what Suyash did years ago
    
    dxy = lpte.dxy
    dz = lpte.dz
    dxy_err = lpte.dxyErr
    dz_err = lpte.dzErr
    
    sigma_xy = dxy/dxy_err
    sigma_z = dz/dz_err
    
    SIP3D = np.sqrt(sigma_xy**2 + sigma_z**2)
    
    return SIP3D





    
