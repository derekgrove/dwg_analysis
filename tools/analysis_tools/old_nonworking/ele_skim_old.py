# Skims and cuts for our samples, signal and background

#PLEASE NOTE: The object returned from the skim functions are 
# Boolean masks, *not* the filtered list. You use them to create a 
# mask, then feed that mask back into the object you want to cut on

import awkward as ak
import numpy as np


# custodial cuts for jet object in NanoAOD (for delta r matching to electrons)
def jet_cuts(jet_obj):
    """ Apply selection cuts to jets for later use with delta r matching to electrons """
    
    mask = (
        (jet_obj.jetId >= 3) &
        (jet_obj.pt > 10) &
        (np.abs(jet_obj.eta) < 3)
    )
    return mask

# should remove these jets from jet collection too ^^^


def delta_r(obj_a, obj_b, threshold):
    """Compute ΔR between electrons and jets and apply a mask for ΔR ≤ 0.2"""
    # written very generally, this calculation is done with axis = 2 so the mask is made relative to/for obj_a
    
    delta_r_matrix = obj_a.metric_table(obj_b)
    
    mask = ak.all(
        delta_r_matrix > threshold,
        axis=2)
    return mask


# These cuts are sequential, by definition, if an electron passes bronze cuts it MUST also pass custodial cuts


def jet_disambig(ele_obj, jet_obj, threshold=0.2):
    
    cleaned_jets = jet_obj[jet_cuts(jet_obj)]
    
    mask = delta_r(ele_obj, cleaned_jets, threshold)
    
    return mask


def custodial_cuts(ele_obj, jet_obj, min_pt_bin=None, max_pt_bin=None):

    mask = (
        (np.abs(ele_obj.eta) < 2.5) &
        (ele_obj.cutBased >= 2) &
        jet_disambig(ele_obj, jet_obj)
    )

    if min_pt_bin is not None:  
        mask &= (min_pt_bin < ele_obj.pt)

    # Apply max_pt_bin if provided
    if max_pt_bin is not None:  
        mask &= (ele_obj.pt <= max_pt_bin)

    return mask


#ideally pass the electrons that pass the above custodial_cuts to this function:




#ideally pass the electrons that pass the above jet_disambiguation into this function:
# delete this maybe? Having this function may lead to misuse, eventually want just the "full_cuts"
def bronze_cuts(ele_obj, min_pt_bin=None, max_pt_bin=None):
    mask = (
        (np.abs(ele_obj.dxy) < 0.05) & 
        (np.abs(ele_obj.dz) < 0.1) &
        (ele_obj.sip3d < 8)  
    )

    if min_pt_bin is not None:  
        mask &= (ele_obj.pt > min_pt_bin)

    if max_pt_bin is not None:  
        mask &= (ele_obj.pt <= max_pt_bin)

    return mask  



# If we want to skip right to bronze cut electrons, use the below, feed it the original uncut electrons and jets

def full_bronze_cuts(ele_obj, jet_obj, min_pt_bin=None, max_pt_bin=None):

    cleaned_jets = jet_obj[jet_cuts(jet_obj)]

    mask = (
        custodial_cuts(ele_obj, min_pt_bin, max_pt_bin) &
        (np.abs(ele_obj.dxy) < 0.05) & 
        (np.abs(ele_obj.dz) < 0.1) &
        (ele_obj.sip3d < 8) & 
        jet_disambig(ele_obj, cleaned_jets, 0.2) # checks ΔR for electron with every jet in event, makes sure ΔR isn't within 'threshold' distance
    )

    return mask


def full_silver_cuts(ele_obj, jet_obj, min_pt_bin=None, max_pt_bin=None):

    mask = (
        full_bronze_cuts(ele_obj, jet_obj, min_pt_bin=None, max_pt_bin=None)
    )
    return mask
    





























