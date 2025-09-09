# Define our skims or (categories) for Electrons, Muons, LowPtElectrons
import json
from .lep_cuts import *
from .vid_unpacked import *



####################################################################
# functions that take the lepton collections, checks if the lepton is baseline, gold, etc., adds a boolean to it if so. Thats it.



def tag_ele_quality(ele): #use on raw ele collection

    """
    Add an 'isBaseline', 'isGold', 'isSilver', 'isBronze' field to each Electron based on cuts.
    """
    
    baseline_mask = (
        pt_selection(ele, 7, 1.4e12) &
        eta_2p5(ele) &
        loose_sip3d(ele) &
        dxy_0p05(ele) &
        dz_0p1(ele) &
        pfRelIso(ele, tight=False) &
        miniIso(ele, tight=False) &
        loose_no_iso_hoe(ele)
    )

    new_baseline_mask = (
        pt_selection(ele, 7, 1.4e12) &
        eta_2p5(ele) &
        loose_sip3d(ele) &
        dxy_0p05(ele) &
        dz_0p1(ele) &
        pfRelIso(ele, tight=False) &
        miniIso(ele, tight=False) &
        loose_minus_iso_hoe(ele)
    )

    gold_mask = (
        baseline_mask &
        tight_sip3d(ele) &
        pfRelIso(ele, tight=True) &
        miniIso(ele, tight=True) &
        tight_no_iso_hoe(ele)
    )

    silver_mask = (
        baseline_mask &
        ~tight_sip3d(ele) &
        pfRelIso(ele, tight=True) &
        miniIso(ele, tight=True) &
        tight_no_iso_hoe(ele)
    )

    bronze_mask = (
        baseline_mask &
        ~(gold_mask | silver_mask)
    )
    
    # Add new fields: isGold, isSilver, isBronze
    ele = ak.with_field(ele, baseline_mask, "isBaseline")
    ele = ak.with_field(ele, new_baseline_mask, "isBaseline_new")
    ele = ak.with_field(ele, gold_mask, "isGold")
    ele = ak.with_field(ele, silver_mask, "isSilver")
    ele = ak.with_field(ele, bronze_mask, "isBronze")

    return ele


####################################################################
# LowPtElectrons


def tag_lpte_quality(lpte): #use on raw lpte collection

    """
    Add an 'isBaseline', 'isGold', 'isSilver', 'isBronze' field to each LowPtElectron based on cuts.
    """
    baseline_mask = (
        pt_selection(lpte, 2, 7) &
        eta_2p5(lpte) &
        conv_veto(lpte) &
        loose_sip3d_lpte(lpte) &
        dxy_0p05(lpte) &
        dz_0p1(lpte) &
        miniIso(lpte, tight=False) &
        loose_ID(lpte)    
    )

    new_baseline_mask = (
        pt_selection(lpte, 2, 7) &
        eta_2p5(lpte) &
        conv_veto(lpte) &
        loose_sip3d_lpte(lpte) &
        dxy_0p05(lpte) &
        dz_0p1(lpte) &
        miniIso(lpte, tight=False) &
        loose_ID_new(lpte)    
    )

    gold_mask = (
        baseline_mask &
        tight_sip3d_lpte(lpte) &
        miniIso(lpte, tight=True) & 
        central_eta_ID_regions(lpte)
        
    )

    silver_mask = (
        baseline_mask &
        ~tight_sip3d_lpte(lpte) &
        miniIso(lpte, tight=True) &
        central_eta_ID_regions(lpte)
    )

    bronze_mask = (
        baseline_mask &
        ~(gold_mask | silver_mask)
    )
    
    # Add new fields: isGold, isSilver, isBronze
    lpte = ak.with_field(lpte, baseline_mask, "isBaseline")
    lpte = ak.with_field(lpte, new_baseline_mask, "isBaseline_new")
    lpte = ak.with_field(lpte, gold_mask, "isGold")
    lpte = ak.with_field(lpte, silver_mask, "isSilver")
    lpte = ak.with_field(lpte, bronze_mask, "isBronze")


    return lpte



####################################################################
# Muons:

def tag_muon_quality(muon): #use on raw muon collection

    """
    Add an 'isBaseline', 'isGold', 'isSilver', 'isBronze' field to each Muon based on cuts.
    """
    baseline_mask = (
        pt_selection(muon, 3, 1.4e12) &
        eta_2p5(muon) &
        loose_sip3d(muon) &
        dxy_0p05(muon) &
        dz_0p1(muon) &
        pfRelIso(muon, tight=False) &
        miniIso(muon, tight=False)
    )

    gold_mask = (
        baseline_mask &
        tight_sip3d(muon) &
        pfRelIso(muon, tight=True) &
        miniIso(muon, tight=True) &
        muon_tightID(muon)
    )

    silver_mask = (
        baseline_mask &
        ~tight_sip3d(muon) &
        pfRelIso(muon, tight=True) &
        miniIso(muon, tight=True) &
        muon_tightID(muon)
    )

    bronze_mask = (
        baseline_mask &
        ~(gold_mask | silver_mask)
    )
    
    # Add new fields: isGold, isSilver, isBronze
    muon = ak.with_field(muon, baseline_mask, "isBaseline")
    muon = ak.with_field(muon, gold_mask, "isGold")
    muon = ak.with_field(muon, silver_mask, "isSilver")
    muon = ak.with_field(muon, bronze_mask, "isBronze")


    return muon
