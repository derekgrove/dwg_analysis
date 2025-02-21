import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema
# my tools:
from analysis_tools.parent_filter import prim_ele
from analysis_tools.ele_skim import custodial_cuts as ele_cust
from analysis_tools.ele_skim import jet_disambig as ele_disambig
from analysis_tools.ele_skim import bronze_cuts as ele_bronze
from analysis_tools.ele_skim import full_bronze_cuts as full_ele_bronze

#import hist
import dask
import hist.dask as dah


class SignalProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        total_entries = ak.num(events, axis=0)

        #lpte = events.LowPtElectron
        #count_lpte = ak.sum(ak.num(lpte))
        
        ele = events.Electron
        count_ele = ak.sum(ak.num(ele))
        
        #muons = events.Muon
        #count_muons = ak.sum(ak.num(muons))
        
        jets = events.Jet # need to give list of Jets to our bronze cuts for delta r matching:

        # begin GenParent cuts:

        filtered_ele = prim_ele(ele)
        filtered_ele = filtered_ele[filtered_ele.genPartFlav == 1]

        count_filtered_ele = ak.sum(ak.num(filtered_ele))
        
        # begin custodial cuts:
        
        #cust_ele = filtered_ele[ele_cust(filtered_ele)]
        cust_ele = filtered_ele[ele_cust(filtered_ele)]
        count_cust_ele = ak.sum(ak.num(cust_ele))

        disambig_ele = cust_ele[ele_disambig(cust_ele, jets)]
        count_disambig_ele = ak.sum(ak.num(disambig_ele))

        bronze_ele = disambig_ele[ele_bronze(disambig_ele)]
        count_bronze_ele = ak.sum(ak.num(bronze_ele))

        #test that the below (full bronze cuts) is equivalent to the sequential above
        full_bronze_test = ele[full_ele_bronze(ele, jets)]
        count_full_bronze_test = ak.sum(ak.num(full_bronze_test))
        
        # define histograms to fill:

        #hists of full distributions

        #no cuts:
        
        ele_mini_iso = dah.Hist.new.Regular(100, 0, 50, name = "mini_iso").Double()
        ele_mini_iso.fill(mini_iso = ak.flatten(ele.miniPFRelIso_all))

        

        
        

        ele_num = calc_num(bronze_ele, ele_cut_list, ele_pts)
        
        output = {
            "counts": {
                "total_entries": total_entries,
                "count_ele": count_ele,
                
            },
        
            "calculations": {
                
            },
        
            "plots": {
                "ele_mini_iso": ele_mini_iso,
                
                
            },
        
            "tests": {
                
            }  # Empty for now, but you can add test-related variables
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
        