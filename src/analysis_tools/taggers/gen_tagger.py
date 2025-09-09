# Define our skims or (categories) for Electrons, Muons, LowPtElectrons
import json
#from .lep_cuts import *

from gen_filter import *

# This tagger is only to be used on MC files that have gen info, won't work on data

# ###################################################################
# functions that take the lepton collections, add what type of gen it was to the collection, thats it.

def tag_gen_flags(obj, signal_func): #signal function is from lep_cuts, either 'ele_gen', 'lpte_gen', or 'muon_gen'
#def tag_gen_flags(obj):
    """Add isSignal, isLightFake, isHeavyFake, isFromTau to a lepton object."""
    
    signal_mask = primary_mask(obj) & signal_func(obj)
    
    lfake_mask = light_fake_mask(obj) & signal_func(obj) #I added these signal_func Sep 9th 2025, maybe remove
    hfake_mask = heavy_fake_mask(obj) & signal_func(obj) #and here,
    #tfake_mask = gflav15(obj)

    obj = ak.with_field(obj, signal_mask, "isSignal")
    obj = ak.with_field(obj, lfake_mask, "isLightFake")
    obj = ak.with_field(obj, hfake_mask, "isHeavyFake")
    #obj = ak.with_field(obj, tfake_mask, "isTauFake")
    
    return obj

def primary_mask(obj): return (gflav1(obj) & gen_parent(obj))
    
def light_fake_mask(obj): return gflav0(obj)

def heavy_fake_mask(obj): return heavy_decay(obj)