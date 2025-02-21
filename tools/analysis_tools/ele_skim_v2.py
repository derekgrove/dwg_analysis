# Skims and cuts for our samples, signal and background

#PLEASE NOTE: The object returned from the skim functions are 
# Boolean masks, *not* the filtered list. You use them to create a 
# mask, then feed that mask back into the object you want to cut on

import awkward as ak
import numpy as np
import hist.dask as dah



# custodial cuts for jet object in NanoAOD (for delta r matching to electrons)
def jet_cuts(jet_obj):
    """ Apply selection cuts to jets for later use with delta r matching to electrons """
    
    mask = (
        (jet_obj.jetId >= 3) &
        (jet_obj.pt > 10) &
        (np.abs(jet_obj.eta) < 3)
    )
    return mask

# Alice: should remove these jets from jet collection too ^^^

def delta_r_mask(obj_a, obj_b, threshold):
    """Compute ΔR between electrons and jets and apply a mask for ΔR ≤ 0.2"""
    # written very generally, this calculation is done with axis = 2 so the mask is made relative to/for obj_a
    
    delta_r_matrix = obj_a.metric_table(obj_b)
    
    mask = ak.all(
        delta_r_matrix > threshold,
        axis=2)
    return mask

def delta_r(obj_a, obj_b):
    """Compute ΔR between electrons and jets and apply a mask for ΔR ≤ 0.2"""
    # written very generally, this calculation is done with axis = 2 so the mask is made relative to/for obj_a
    
    delta_r_matrix = obj_a.metric_table(obj_b)

    return delta_r_matrix

def delta_r_electron_pairs(ele_obj):
    """
    Computes ΔR between unique pairs of electrons in an event.
    Returns the smallest ΔR per electron pair.
    """
    # Get unique electron pairs
    ele_pairs = ak.combinations(ele_obj, 2, fields=["ele1", "ele2"])

    # Compute ΔR between electron pairs
    delta_r_matrix = ele_pairs.ele1.metric_table(ele_pairs.ele2)

    # Find the smallest ΔR per electron pair
    min_delta_r = ak.min(delta_r_matrix, axis=1, initial=1e6)  # Avoid empty lists issue

    return min_delta_r

def test_comb(ele_obj):

    ak.combinations(ele_obj, 2).show()



def jet_disambig(ele_obj, jet_obj, threshold=0.2):
    
    cleaned_jets = jet_obj[jet_cuts(jet_obj)]
    
    mask = delta_r_mask(ele_obj, cleaned_jets, threshold)
    
    return mask


def vidUnpackedWP(obj):
    """
    Return a dictionary of the cuts in the electron cutBasedID,
    e.g. results["GsfEleEInverseMinusPInverseCut"] will be 0 (fail), 1, 2, 3, or 4 (tight)
    """
    results = {}
    for name, shift in zip(
        [
            "MinPtCut",
            "GsfEleSCEtaMultiRangeCut",
            "GsfEleDEtaInSeedCut",
            "GsfEleDPhiInCut",
            "GsfEleFull5x5SigmaIEtaIEtaCut",
            "GsfEleHadronicOverEMEnergyScaledCut",
            "GsfEleEInverseMinusPInverseCut",
            "GsfEleRelPFIsoScaledCut",
            "GsfEleConversionVetoCut",
            "GsfEleMissingHitsCut",
        ],
        range(0, 28, 3),
    ):
        results[name] = (obj.vidNestedWPBitmap >> shift) & 0b111
    return results


def vidUnpackedWPSelection(electrons, level):
    """Return a dictionary of boolean masks for the electron cutBasedID,
    e.g. results["GsfEleEInverseMinusPInverseCut"] will be True if the result value is >= level
    """
    results = {}
    for name, cut_level in vidUnpackedWP(electrons).items():
        results[name] = cut_level >= level
        
    return results



def count_events(events, ele_obj):
    ele_counts = ak.num(ele_obj)
    
    event_count = ak.count_nonzero(ele_counts >= 1)
    return event_count

def count_ele(ele_obj):
    ele_counts = ak.num(ele_obj)

    counts = ak.sum(ele_counts)
    return counts

def count_events_and_ele(events, ele_obj):
    
    return count_events(events, ele_obj), count_ele(ele_obj)


def veto_minus_iso_mask(ele_obj):
    
    vid_Unpacked = vidUnpackedWP(ele_obj)

    mask = (
        (vid_Unpacked['MinPtCut'] >= 1) & 
        (vid_Unpacked['GsfEleSCEtaMultiRangeCut'] >= 1) &
        (vid_Unpacked['GsfEleDEtaInSeedCut'] >= 1) &
        (vid_Unpacked['GsfEleDPhiInCut'] >= 1) &
        (vid_Unpacked['GsfEleFull5x5SigmaIEtaIEtaCut'] >= 1) &
        (vid_Unpacked['GsfEleHadronicOverEMEnergyScaledCut'] >= 1) &
        (vid_Unpacked['GsfEleEInverseMinusPInverseCut'] >= 1) &
        (vid_Unpacked['GsfEleConversionVetoCut'] >= 1) &
        (vid_Unpacked['GsfEleMissingHitsCut'] >= 1)
    )

    return mask



def baseline_mask(ele_obj):
    
    mask = (
        (veto_minus_iso_mask(ele_obj)) &  # Ensuring this function works properly
        (ele_obj.sip3d < 8) & 
        (np.abs(ele_obj.dxy) < 0.05) & 
        (np.abs(ele_obj.dz) < 0.1)
    )
    
    return mask



def baseline_plus_mask(ele_obj, jet_obj):

    mask = (
        baseline_mask(ele_obj) &
        (np.abs(ele_obj.eta) < 2.5) &
        jet_disambig(ele_obj, jet_obj)
    )

    return mask


"""
def bronze_mask(ele_obj, jet_obj):

    mask = (
        baseline_plus_mask(ele_obj, jet_obj) &
        (
            ((ele_obj.cutBased == 4) & ((ele_obj.pfRelIso03_all * ele_obj.pt) > 4) & ((ele_obj.miniPFRelIso_all * ele_obj.pt) > 4)) |
            ((ele_obj.cutBased < 4) & ((ele_obj.pfRelIso03_all * ele_obj.pt) < 4) & ((ele_obj.miniPFRelIso_all * ele_obj.pt) < 4))
        )
    )

    return mask
"""


def silver_mask(ele_obj, jet_obj):

    mask = (
        baseline_plus_mask(ele_obj, jet_obj) &
        (ele_obj.cutBased == 4) &
        ((ele_obj.pfRelIso03_all * ele_obj.pt) <= 4) &
        ((ele_obj.miniPFRelIso_all * ele_obj.pt) <= 4) &
        (ele_obj.sip3d > 2)
        )

    return mask



def gold_mask(ele_obj, jet_obj):

    mask = (
        baseline_plus_mask(ele_obj, jet_obj) &
        (ele_obj.cutBased == 4) &
        ((ele_obj.pfRelIso03_all * ele_obj.pt) <= 4) &
        ((ele_obj.miniPFRelIso_all * ele_obj.pt) <= 4) &
        (ele_obj.sip3d <= 2)
        )

    return mask


def bronze_mask(ele_obj, jet_obj):
    # Keep only those NOT in gold or silver
    not_gold_silver_mask = ~(gold_mask(ele_obj, jet_obj) | silver_mask(ele_obj, jet_obj))
                             
    mask = (
        baseline_plus_mask(ele_obj, jet_obj) &
        not_gold_silver_mask
    )
    
    return mask
    
"""
def veto_minus_iso(ele_obj, threshold = 1):
# loop through the entire bitmap in steps of 3 bits, extracting each cut's bits, skipping the 7th cut (iso)
    for i, shift in enumerate(range(0, 28, 3)):
        if i == 7:
            continue
            
        extracted_bits = (ele_obj.vidNestedWPBitmap >> shift) & 0b111
        cut_bits.append(extracted_bits)

    # now check that each cut is equal to or greater than 1 (Veto ID)

    #result = ak.all(bits >= 1 for bits in cut_bits)

    results = all(bits >= threshold for bits in cut_bits)
    
    return ele_mask

"""
    
##### Define full cuts here, that utilize the above masks, for convenience #####



def veto_minus_iso_cut(ele_obj):

    return ele_obj[veto_minus_iso_mask(ele_obj)]


def baseline_cut(ele_obj):

    return ele_obj[baseline_mask(ele_obj)]


def baseline_plus_cut(ele_obj, jet_obj):

    return ele_obj[baseline_plus_mask(ele_obj, jet_obj)]


def bronze_cut(ele_obj, jet_obj):

    return ele_obj[bronze_mask(ele_obj, jet_obj)]


def silver_cut(ele_obj, jet_obj):

    return ele_obj[silver_mask(ele_obj, jet_obj)]


def gold_cut(ele_obj, jet_obj):

    return ele_obj[gold_mask(ele_obj, jet_obj)]
        


def make_electron_histograms(ele_obj, label="default"):
    """
    Creates and fills histograms for an electron collection.

    Parameters:
    - ele_obj: Awkward Array of electrons
    - label: String label for the histograms (default="filtered")

    Returns:
    - Dictionary of histograms containing:
      - pT histogram
      - eta histogram
      - 2D histograms for pT vs miniISO, pT vs pfRelIso, and pT vs sip3D
    """

    # Define histograms
    histograms = {
        f"{label}_pt": dah.Hist.new.Regular(100, 0, 50, name="pT", underflow=False, overflow=False).Double(),
        f"{label}_eta": dah.Hist.new.Regular(100, -3, 3, name="eta").Double(),
        f"{label}_pt_vs_mini_iso": (
            dah.Hist.new
            .Regular(100, 5, 30, name="pT")
            .Regular(100, 0, 10, name="mini_iso_pt")
            .Double()
        ),
        f"{label}_pt_vs_pfrel_iso": (
            dah.Hist.new
            .Regular(100, 5, 30, name="pT")
            .Regular(100, 0, 10, name="pfrel_iso_pt")
            .Double()
        ),
        f"{label}_pt_vs_sip3d": (
            dah.Hist.new
            .Regular(100, 5, 30, name="pT")
            .Regular(100, 0, 9, name="sip3D")
            .Double()
        ),
    }

    # Fill histograms
    histograms[f"{label}_pt"].fill(pT=ak.flatten(ele_obj.pt))
    histograms[f"{label}_eta"].fill(eta=ak.flatten(ele_obj.eta))
    histograms[f"{label}_pt_vs_mini_iso"].fill(
        pT=ak.flatten(ele_obj.pt), mini_iso_pt=ak.flatten(ele_obj.miniPFRelIso_all*ele_obj.pt)
    )
    histograms[f"{label}_pt_vs_pfrel_iso"].fill(
        pT=ak.flatten(ele_obj.pt), pfrel_iso_pt=ak.flatten(ele_obj.pfRelIso03_all*ele_obj.pt)
    )
    histograms[f"{label}_pt_vs_sip3d"].fill(
        pT=ak.flatten(ele_obj.pt), sip3D=ak.flatten(ele_obj.sip3d)
    )

    return histograms




