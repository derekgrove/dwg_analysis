# Define our skims or (categories) for Electrons, Muons, LowPtElectrons
import json
#from .lep_cuts import *
from .vid_unpacked import *
import numpy as np
import awkward as ak

####################################################################
# functions that take the lepton collections, checks if the lepton is baseline, gold, etc., adds a boolean to it if so. Thats it.

def tag_ele_quality(ele):  # use on raw Electron collection (Awkward/NanoEvents)
    
    """
    Add 'baseline', 'gold', 'silver', 'bronze' boolean fields to each electron.
    (and some testing fields for vid_unpacked)
    """

    # --- Veto masks defined in vid_unpacked
    ele['veto_minus_iso']     = veto_minus_iso(ele)
    ele['veto_minus_hoe']     = veto_minus_hoe(ele)
    ele['veto_minus_iso_hoe'] = veto_minus_iso_hoe(ele)
    ele['veto']               = veto(ele)

    # --- Loose masks defined in vid_unpacked
    ele['loose_minus_iso']     = loose_minus_iso(ele)
    ele['loose_minus_hoe']     = loose_minus_hoe(ele)
    ele['loose_minus_iso_hoe'] = loose_minus_iso_hoe(ele)

    

    # define variables
    abs_eta   = np.abs(ele.eta)
    abs_dxy   = np.abs(ele.dxy)
    abs_dz    = np.abs(ele.dz)
    pt        = ele.pt
    iso03pt   = ele.pfRelIso03_all * pt
    miniIsoPt = ele.miniPFRelIso_all * pt

    # --- Baseline selection ---
    baseline_mask = (
        (pt >= 7)
        & ( ((pt >= 10) & (abs_eta < 2.5)) | ((pt < 10) & (abs_eta < 1.442)) )
        & (ele.sip3d < 6)
        & (abs_dxy < 0.05)
        & (abs_dz  < 0.1)
        & (iso03pt   < (20 + 300/pt))
        & (miniIsoPt < (20 + 300/pt))
        & (ele.lostHits == 0)
        & (ele.convVeto == 1) #added this for regular electrons, see how it works
        & loose_minus_iso_hoe(ele)
    )

    # --- Quality tags ---
    gold_mask = (
        baseline_mask
        & (ele.sip3d < 2)
        & (
            ((pt < 20)  & (iso03pt <= 4) & (miniIsoPt <= 4) & tight_minus_iso_hoe(ele))
            |
            ((pt >= 20) & ele.mvaIso_WP90)
        )
    )

    silver_mask = (
        baseline_mask
        & (ele.sip3d >= 2)
        & (
            ((pt < 20)  & (iso03pt <= 4) & (miniIsoPt <= 4) & tight_minus_iso_hoe(ele))
            |
            ((pt >= 20) & ele.mvaIso_WP90)
        )
    )

    gold_silver_mask = (
        baseline_mask
        & (
            ((pt < 20)  & (iso03pt <= 4) & (miniIsoPt <= 4) & tight_minus_iso_hoe(ele))
            |
            ((pt >= 20) & ele.mvaIso_WP90)
        )
    )

    bronze_mask = baseline_mask & ~gold_silver_mask

    ele['isBaseline'] = baseline_mask
    ele['isGold']     = gold_mask
    ele['isSilver']   = silver_mask
    ele['isBronze']   = bronze_mask
    ele['isGoldSilver'] = gold_silver_mask

    return ele


####################################################################
# LowPtElectrons


def tag_lpte_quality(lpte): #use on raw lpte collection

    """
    Add an 'isBaseline', 'isGold', 'isSilver', 'isBronze' field to each LowPtElectron based on cuts.
    """
    
    # define variables
    abs_eta   = np.abs(lpte.eta)
    sip3d     = lpte_sip3d(lpte)
    abs_dxy   = np.abs(lpte.dxy)
    abs_dz    = np.abs(lpte.dz)
    central_eta_ID = (
        ((abs_eta >= 0.8) & (abs_eta < 1.442) & (lpte.ID >= 3)) |
        ((abs_eta < 0.8) & (lpte.ID >= 2.3))
    )
    pt        = lpte.pt
    miniIsoPt = lpte.miniPFRelIso_all * pt

    # --- Baseline selection ---
    baseline_mask = (
        ((pt >= 2) & (pt < 7))
        & (abs_eta < 1.442)
        & (sip3d < 6)
        & (abs_dxy < 0.05)
        & (abs_dz  < 0.1)
        & (miniIsoPt < (20 + 300/pt))
        & (lpte.convVeto == 1)
        & (lpte.lostHits == 0)
        & (lpte.ID >= 1.5)
    )

    # --- Quality tags ---
    gold_mask = (
        baseline_mask
        & (sip3d < 2)
        & (miniIsoPt <= 4)
        & central_eta_ID
    )


    silver_mask = (
        baseline_mask
        & (sip3d >= 2)
        & (miniIsoPt <= 4)
        & central_eta_ID
    )

    gold_silver_mask = (
        baseline_mask
        & (miniIsoPt <= 4)
        & central_eta_ID
    )

    bronze_mask = baseline_mask & ~gold_silver_mask

    lpte['isBaseline'] = baseline_mask
    lpte['isGold']     = gold_mask
    lpte['isSilver']   = silver_mask
    lpte['isBronze']   = bronze_mask
    lpte['isGoldSilver'] = gold_silver_mask


    return lpte


####################################################################
# Muons:

def tag_muon_quality(muon): #use on raw muon collection

    """
    Add 'baseline', 'gold', 'silver', 'bronze' boolean fields to each electron.
    (and some testing fields for vid_unpacked)
    """

    
    # define variables
    abs_eta   = np.abs(muon.eta)
    abs_dxy   = np.abs(muon.dxy)
    abs_dz    = np.abs(muon.dz)
    sip3d = muon.sip3d
    pt        = muon.pt
    iso03pt   = muon.pfRelIso03_all * pt
    miniIsoPt = muon.miniPFRelIso_all * pt
    pfIsoId = muon.pfIsoId
    tight = muon.tightId
    
    
    

    # --- Baseline selection ---
    baseline_mask = (
        (abs_eta < 2.5)
        & (sip3d < 6)
        & (abs_dxy < 0.05)
        & (abs_dz  < 0.1)
        & (iso03pt   < (20 + 300/pt))
        & (miniIsoPt < (20 + 300/pt))
    )

    # --- Quality tags ---
    
    #traditional qualities:

    baseline_tight_mask = ( 
        baseline_mask
        & tight
    )

    ouriso_mask = ( 
        baseline_tight_mask
        & (iso03pt   <= 4)
        & (miniIsoPt <= 4)
    )

    pfIso_0_mask = ( 
        baseline_tight_mask
        & (pfIsoId == 0)
    )

    pfIso_1_mask = ( 
        baseline_tight_mask
        & (pfIsoId == 1)
    )
    pfIso_2_mask = ( 
        baseline_tight_mask
        & (pfIsoId == 2)
    )
    
    pfIso_3_mask = ( 
        baseline_tight_mask
        & (pfIsoId == 3)
    )

    pfIso_4_mask = ( 
        baseline_tight_mask
        & (pfIsoId == 4)
    )

    gold_silver_mask = ( 
        baseline_mask
        & (iso03pt   <= 4)
        & (miniIsoPt <= 4)
        & tight
    )

    gold_mask = (
        gold_silver_mask
        & (sip3d < 2)
    )
        

    silver_mask = (
        gold_silver_mask
        & (sip3d >= 2)
    )

    bronze_mask = baseline_mask & ~gold_silver_mask

    #pfIsoId == 3 (medium) qualities:
    
    gold_silver_mask_pfIsoID_med = (
        baseline_mask
        & (pfIsoId == 3)
        & tight
    )

    gold_mask_pfIsoID_med = (
        gold_silver_mask_pfIsoID_med
        & (sip3d < 2)
    )
        

    silver_mask_pfIsoID_med = (
        gold_silver_mask_pfIsoID_med
        & (sip3d >= 2)
    )

    bronze_mask_pfIsoID_med = baseline_mask & ~gold_silver_mask_pfIsoID_med

    #pfIsoId == 4 (medium) qualities:
    
    gold_silver_mask_pfIsoID_tight = (
        baseline_mask
        & (pfIsoId == 4)
        & tight
    )

    gold_mask_pfIsoID_tight = (
        gold_silver_mask_pfIsoID_tight
        & (sip3d < 2)
    )
        

    silver_mask_pfIsoID_tight = (
        gold_silver_mask_pfIsoID_tight
        & (sip3d >= 2)
    )

    bronze_mask_pfIsoID_tight = baseline_mask & ~gold_silver_mask_pfIsoID_tight

    muon['isBaseline'] = baseline_mask
    muon['isGold']     = gold_mask
    muon['isSilver']   = silver_mask
    muon['isBronze']   = bronze_mask
    muon['isGoldSilver'] = gold_silver_mask

    muon['isBaseline_tight'] = baseline_tight_mask
    muon['pfIso_0'] = pfIso_0_mask
    muon['pfIso_1'] = pfIso_1_mask
    muon['pfIso_2'] = pfIso_2_mask
    muon['pfIso_3'] = pfIso_3_mask
    muon['pfIso_4'] = pfIso_4_mask
    muon['ourIso'] = ouriso_mask
    

    muon['isGold_pfIsoID_med']     = gold_mask_pfIsoID_med
    muon['isSilver_pfIsoID_med']   = silver_mask_pfIsoID_med
    muon['isBronze_pfIsoID_med']   = bronze_mask_pfIsoID_med
    muon['isGoldSilver_pfIsoID_med'] = gold_silver_mask_pfIsoID_med

    muon['isGold_pfIsoID_tight']     = gold_mask_pfIsoID_tight
    muon['isSilver_pfIsoID_tight']   = silver_mask_pfIsoID_tight
    muon['isBronze_pfIsoID_tight']   = bronze_mask_pfIsoID_tight
    muon['isGoldSilver_pfIsoID_tight'] = gold_silver_mask_pfIsoID_tight

    return muon
    


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
