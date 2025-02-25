import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema

# my tools:
from analysis_tools.skimming.parent_filter import prim_ele
from analysis_tools.plotting.make_hist import make_1d_hist
from analysis_tools.plotting.make_hist import make_2d_hist

from analysis_tools.skimming.ele_skim_v2 import (
baseline_cut, gold_cut, count_obj, count_obj_events, count_obj_and_events
)


#from analysis_tools.plotting.make_hist import make_2d_hist


#import hist
import dask
import hist.dask as dah


class TestProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        total_entries = ak.num(events, axis=0)
        
        ele = events.Electron
        jets = events.Jet
        baseline_ele = baseline_cut(ele)

        gold_ele = gold_cut(ele, jets)
        
        hoe_dist_baseline = make_1d_hist(baseline_ele, "hoe", [100, 0, 1.2], label="hoe_dist")
        hoe_dist_gold = make_1d_hist(gold_ele, "hoe", [100, 0, 1.2], label="hoe_dist")

        baseline_hoe_pt_dist = make_2d_hist(baseline_ele, "pt", [60,5,35], "hoe", [60,0,1.2], label_a="pt", label_b="hoe")
        gold_hoe_pt_dist = make_2d_hist(gold_ele, "pt", [60,5,35], "hoe", [60,0,1.2], label_a="pt", label_b="hoe")
        
        #(obj, attribute, [bins, xmin, xmax], label="axis_label"):
        ele_pt_dist = make_1d_hist(ele, "pt", [1000, 5, 200], label="pt_dist")

        #make_2d_hist(obj, attribute_a, binning_a, attribute_b, binning_b, label_a="axis_label_a", label_b="axis_label_b")
        ele_pt_eta_dist = make_2d_hist(ele, "pt", [100,0,10], "eta", [100,-3,3], label_a="pt", label_b="eta")

        count_obj_test = count_obj(ele)
        count_obj_events_test = count_obj_events(ele, events)
        count_obj_and_events_test = count_obj_and_events(ele, events)
        
        jets = events.Jet # need to give list of Jets to our bronze cuts for delta r matching:

        
        output = {
            "counts": {
                "count_obj_test": count_obj_test,
                "count_obj_events_test": count_obj_events_test,
                "count_obj_and_events_test": count_obj_and_events_test,
                
            },

            "pt_binned": {

            },
        
            "calculations": {
                
            },
        
            "plots": {
                "ele_pt_dist": ele_pt_dist,
                "ele_pt_eta_dist": ele_pt_eta_dist,
                "hoe_dist_baseline": hoe_dist_baseline,
                "hoe_dist_gold": hoe_dist_gold,
                "baseline_hoe_pt_dist": baseline_hoe_pt_dist,
                "gold_hoe_pt_dist": gold_hoe_pt_dist,
                
                
            },
        
            "tests": {
                
            }
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
