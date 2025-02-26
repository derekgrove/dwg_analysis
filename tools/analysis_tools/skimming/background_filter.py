# Parent filter for our signal samples

# We are concerned with primary electrons, so:
# Only allows W's, Z's, and sleptons through

import awkward as ak
import numpy as np

def parent_mask(ele_object):
    # ele_object could be events.Electron or events.LowPtElectron

    is_W = (abs(ele_object.matched_gen.distinctParent.pdgId) == 24)
    is_W_clean = ak.fill_none(is_W, False)
    
    is_Z = (ele_object.matched_gen.distinctParent.pdgId == 23)
    is_Z_clean = ak.fill_none(is_Z, False)

    is_sel = ((ele_object.matched_gen.distinctParent.pdgId == 1000011) | 
              (ele_object.matched_gen.distinctParent.pdgId == 2000011))
    is_sel_clean = ak.fill_none(is_sel, False)

    is_smu = ((ele_object.matched_gen.distinctParent.pdgId == 1000013) | 
              (ele_object.matched_gen.distinctParent.pdgId == 2000013))
    is_smu_clean = ak.fill_none(is_smu, False)

    is_LSP = (ele_object.matched_gen.distinctParent.pdgId == 1000022)
    is_LSP_clean = ak.fill_none(is_LSP, False)

    is_sLSP = (ele_object.matched_gen.distinctParent.pdgId == 1000023)
    is_sLSP_clean = ak.fill_none(is_sLSP, False)

    is_LCG = (abs(ele_object.matched_gen.distinctParent.pdgId) == 1000024)
    is_LCG_clean = ak.fill_none(is_LCG, False)

    all_filters = (is_W_clean | is_Z_clean | is_sel_clean | 
                   is_smu_clean | is_LSP_clean | is_sLSP_clean | is_LCG_clean)

    return all_filters #returns a boolean mask


def gen_kinematic_mask(ele_obj):
    
    ele_mask = ((ele_obj.matched_gen.pt > 4.5) & (np.abs(ele_obj.matched_gen.eta) < 3))
    ele_mask_clean = ak.fill_none(ele_mask, False)
    
    return ele_mask_clean


def primary_vertex_mask(ele_obj):

    ele_mask = (ele_obj.genPartFlav == 1)

    return ele_mask


# cutting functions below, apply all masks (or combination):


def filter_cut(ele_obj):

    return ele_obj[
        parent_mask(ele_obj) & 
        gen_kinematic_mask(ele_obj) & 
        primary_vertex_mask(ele_obj)
    ]

    
