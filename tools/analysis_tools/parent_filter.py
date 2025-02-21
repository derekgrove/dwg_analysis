# Parent filter for our signal samples

# We are concerned with primary electrons, so:
# Only allows W's, Z's, and sleptons through

import awkward as ak

def prim_ele(electron_object):
    # electron_object could be events.Electron or events.LowPtElectron

    is_W = (abs(electron_object.matched_gen.distinctParent.pdgId) == 24)
    is_W_clean = ak.fill_none(is_W, False)
    
    is_Z = (electron_object.matched_gen.distinctParent.pdgId == 23)
    is_Z_clean = ak.fill_none(is_Z, False)

    is_sel = ((electron_object.matched_gen.distinctParent.pdgId == 1000011) | 
              (electron_object.matched_gen.distinctParent.pdgId == 2000011))
    is_sel_clean = ak.fill_none(is_sel, False)

    is_smu = ((electron_object.matched_gen.distinctParent.pdgId == 1000013) | 
              (electron_object.matched_gen.distinctParent.pdgId == 2000013))
    is_smu_clean = ak.fill_none(is_smu, False)

    is_LSP = (electron_object.matched_gen.distinctParent.pdgId == 1000022)
    is_LSP_clean = ak.fill_none(is_LSP, False)

    is_sLSP = (electron_object.matched_gen.distinctParent.pdgId == 1000023)
    is_sLSP_clean = ak.fill_none(is_sLSP, False)

    is_LCG = (abs(electron_object.matched_gen.distinctParent.pdgId) == 1000024)
    is_LCG_clean = ak.fill_none(is_LCG, False)

    all_filters = (is_W_clean | is_Z_clean | is_sel_clean | 
                   is_smu_clean | is_LSP_clean | is_sLSP_clean | is_LCG_clean)

    primary_electrons = electron_object[all_filters]

    return primary_electrons #returns a list of electrons, NOT A BOOLEAN MASK