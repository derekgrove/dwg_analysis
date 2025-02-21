# Skims and cuts for our samples, signal and background

#PLEASE NOTE: The object returned from the skim functions are 
# Boolean masks, *not* the filtered list. You use them to create a 
# mask, then feed that mask back into the object you want to cut on

import awkward as ak
import numpy as np


# custodial cuts for jet object in NanoAOD (for delta r matching to electrons)
def jet_cuts(object):
    """ Apply selection cuts to jets for later use with delta r matching to electrons """
    
    mask = (
        (object.jetId >= 3) &
        (object.pt > 20) &
        (np.abs(object.eta) < 2.4)
    )
    return mask

# written very generally, this calculation is done with axis = 2 so the mask is made relative to/for obj_a
def delta_r(obj_a, obj_b, threshold):
    """Compute ΔR between electrons and jets and apply a mask for ΔR ≤ 0.2"""
    
    delta_r_matrix = obj_a.metric_table(obj_b)
    
    mask = ak.all(
        delta_r_matrix <= threshold,
        axis=2)
    return mask

#should remove jet too, when looking at jets ^^^


# in order to have delta r matching to jets be part of our custodial cuts, need to define our custodial cuts
# to accept the electron lists we want but also the jets list from NanoAOD


def sip3D(dxy, dz, dxyErr, dzErr):
    sigma_xy = dxy/dxyErr
    sigma_z = dz/dzErr
    return np.sqrt(sigma_xy**2 + sigma_z**2)

# The expectation is you will only pass a LowPtElectron object into this function and a Jet object:

def custodial_cuts(obj):
    """ Apply custodial cuts to object """
    (np.abs(lpte_obj.eta) < 2.4)
    
    
def lpte_cuts(lpte_obj, jet_obj, min_pt_bin=None, max_pt_bin=None):  
    """ Apply selection cuts to low-pT electrons with optional pt bin cuts. """
                                                          
    mask = (
        (np.abs(lpte_obj.eta) < 2.4) &
        (sip3D(lpte_obj.dxy, lpte_obj.dz, lpte_obj.dxyErr, lpte_obj.dzErr) < 8) & 
        (np.abs(lpte_obj.dxy) < 0.05) & 
        (np.abs(lpte_obj.dz) < 0.1) & 
        (lpte_obj.miniPFRelIso_all < (0.194 + (0.535 / lpte_obj.pt))) &
        delta_r(lpte_obj, jet_obj)
    )

    # Apply min_pt_bin if provided
    if min_pt_bin is not None:  
        mask &= (object.pt > min_pt_bin)
        
    # Apply max_pt_bin if provided
    if max_pt_bin is not None:  
        mask &= (object.pt <= max_pt_bin)
    
    return mask


# The expectation is you will only pass an Electron object and a Jet object in this function:

def ele_cuts(ele_obj, jet_obj, min_pt_bin=None, max_pt_bin=None):  
    """ Apply selection cuts to electrons with optional pt bin cuts. """
                                                          
    mask = (
        (np.abs(ele_obj.eta) < 2.4) &
        (ele_obj.sip3d < 8) & 
        (np.abs(ele_obj.dxy) < 0.05) & 
        (np.abs(ele_obj.dz) < 0.1) & 
        (ele_obj.pfRelIso03_all < (0.194 + (0.535 / ele_obj.pt))) &
        delta_r(ele_obj, jet_obj)
    )

    # Apply min_pt_bin if provided
    if min_pt_bin is not None:  
        mask &= (object.pt > min_pt_bin)

    # Apply max_pt_bin if provided
    if max_pt_bin is not None:  
        mask &= (object.pt <= max_pt_bin)
    
    return mask



# custodial cuts for Muons in NanoAOD
def mu_cuts(object):
    return (
            (np.abs(object.eta) < 2.4) &
            #(object.pt < max_bin_width) &
            (object.sip3d < 8) & 
            (np.abs(object.dxy) < 0.05) & 
            (np.abs(object.dz) < 0.1) & 
            (object.pfRelIso03_all < (0.194 + (0.535 / object.pt)))
        )
    

    
