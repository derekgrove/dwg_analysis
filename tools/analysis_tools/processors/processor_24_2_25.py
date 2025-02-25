import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema
# my tools:
from analysis_tools.skimming.parent_filter import prim_ele
from analysis_tools.skimming.ele_skim_v2 import (
    veto_minus_iso_cut,
    baseline_cut,
    baseline_plus_cut,
    bronze_cut,
    silver_cut,
    gold_cut,
    count_obj_events,
    count_obj,
    count_obj_and_events,
    delta_r,
)

#import hist
import dask
import hist.dask as dah


class MyProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        ele = events.Electron
        
        total_entries = count_obj_events(ele, events)
        total_entries_oldmethod = ak.num(events, axis=0)
        
        total_ele = count_obj(ele)

        test_1 = ak.num(ele)
        test_2 = ak.count_nonzero(test_1)
        
        jets = events.Jet # need to give list of Jets to our bronze cuts for delta r matching:

        
        
        
        
        # begin GenParent filtering cuts: #######

        

        # replace regular electron collection with genParent filtered and genFlav 1:
        
        

        # begin baseline cuts: #######
        
    

        
        # begin baseline+ cuts: #######

        
        # begin bronze, silver, gold cuts: ######

        
        #make plots here:

        #we have these categories of electrons to make plots for:
        # filtered_ele, baseline_ele, baseline_plus_ele, bronze_ele, silver_ele, gold_ele

        
        

        
        lpte_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20]
        ele_pts = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 100]

        # "cut lists", NanoAOD variable then the value to cut on:

        
        
        
        output = {
            "counts": {
                "total_entries": total_entries,
                "total_entries_oldmethod": total_entries_oldmethod,
                "total_ele": total_ele,
                "test_1": test_1,
                "test_2": test_2,
                
            },

            "pt_binned": {

            },
        
            "calculations": {
                
            },
        
            "plots": {
                
                
            },
        
            "tests": {
                
            }
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
