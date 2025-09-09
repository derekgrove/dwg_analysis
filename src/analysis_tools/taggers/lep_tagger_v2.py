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
        veto_no_iso_hoe(ele)
    )
    
    baseline_mask_template = (
        pt_selection(ele, 7, 1.4e12) &
        eta_2p5(ele) &
        loose_sip3d(ele) &
        dxy_0p05(ele) &
        dz_0p1(ele) &
        pfRelIso(ele, tight=False) &
        miniIso(ele, tight=False)
    )

    baseline_mask_VETO = (
        baseline_mask_template &
        cutbased_VETO(ele)
    )

    baseline_mask_no_iso = (
        baseline_mask_template &
        veto_minus_iso(ele)
    )

    baseline_mask_no_hoe = (
        baseline_mask_template &
        veto_minus_hoe(ele)
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

    gold_silver_mask = (
        baseline_mask &
        pfRelIso(ele, tight=True) &
        miniIso(ele, tight=True) &
        tight_no_iso_hoe(ele)
    )

    gold_silver_mask_template = (
        pfRelIso(ele, tight=True) &
        miniIso(ele, tight=True)
    )

    gold_silver_mask_TIGHT = (
        gold_silver_mask_template &
        #baseline_mask_VETO &
        baseline_mask &
        cutbased_TIGHT(ele)
    )

    gold_silver_mask_no_iso = (
        gold_silver_mask_template &
        #baseline_mask_no_iso &
        baseline_mask &
        tight_no_iso(ele)
    )

    gold_silver_mask_no_hoe = (
        gold_silver_mask_template &
        #baseline_mask_no_hoe &
        baseline_mask &
        tight_no_hoe(ele)
    )

    #gold_silver_mask_tightCharge_1 = (
    #    gold_silver_mask_template &
    #    baseline_mask &
    #    tightCharge_1(ele)
    #)
    gold_silver_mask_tightCharge_1 = (
        gold_silver_mask &
        tightCharge_1(ele)
    )

    #gold_silver_mask_tightCharge_2 = (
    #    gold_silver_mask_template &
    #    baseline_mask &
    #    tightCharge_2(ele)
    #)
    
    gold_silver_mask_tightCharge_2 = (
        gold_silver_mask &
        tightCharge_2(ele)
    )

    gold_silver_mask_mvaIso_WP80 = (
        gold_silver_mask_template &
        baseline_mask &
        mvaIso_WP80(ele)
    )

    gold_silver_mask_mvaIso_WP90 = (
        gold_silver_mask_template &
        baseline_mask &
        mvaIso_WP90(ele)
    )

    mvaIso_WP80_mask = (
        baseline_mask &
        mvaIso_WP80(ele)
    )

    mvaIso_WP90_mask = (
        baseline_mask &
        mvaIso_WP90(ele)
    )
    
    # Add new fields: isGold, isSilver, isBronze
    ele = ak.with_field(ele, gold_silver_mask, "isGoldSilver")
    ele = ak.with_field(ele, gold_silver_mask_TIGHT, "isGold_silver_TIGHT")
    ele = ak.with_field(ele, gold_silver_mask_no_iso, "isGold_silver_no_iso")
    ele = ak.with_field(ele, gold_silver_mask_no_hoe, "isGold_silver_no_hoe")
    ele = ak.with_field(ele, gold_silver_mask_tightCharge_1, "isGold_silver_tightCharge_1")
    ele = ak.with_field(ele, gold_silver_mask_tightCharge_2, "isGold_silver_tightCharge_2")
    ele = ak.with_field(ele, gold_silver_mask_mvaIso_WP80, "isGold_silver_mvaIso_WP80")
    ele = ak.with_field(ele, gold_silver_mask_mvaIso_WP90, "isGold_silver_mvaIso_WP90")
    ele = ak.with_field(ele, mvaIso_WP80_mask, "isMvaIso_WP80")
    ele = ak.with_field(ele, mvaIso_WP90_mask, "isMvaIso_WP90")
    

    ele = ak.with_field(ele, baseline_mask_VETO, "isBaseline_VETO")
    ele = ak.with_field(ele, baseline_mask_no_iso, "isBaseline_no_iso")
    ele = ak.with_field(ele, baseline_mask_no_hoe, "isBaseline_no_hoe")
    
    ele = ak.with_field(ele, baseline_mask, "isBaseline")
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
        loose_sip3d_lpte(lpte) &
        dxy_0p05(lpte) &
        dz_0p1(lpte) &
        miniIso(lpte, tight=False) &
        loose_ID(lpte)
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
