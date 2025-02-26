import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema

# my tools:
#from analysis_tools.skimming.parent_filter import prim_ele

from analysis_tools.skimming.parent_filter import (
    filter_cut, gen_kinematic_mask, primary_vertex_mask, parent_mask
)

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

        print(ele.matched_gen.fields)

        filter_ele = filter_cut(ele)
        filter_ele_count = count_obj(filter_ele)

        test_gen_kinematic_ele = ele[gen_kinematic_mask(ele)]
        count_gen_kin = count_obj(test_gen_kinematic_ele)
        
        test_primary_vertex_ele = ele[primary_vertex_mask(ele)]
        count_primary_vertex = count_obj(test_primary_vertex_ele)
        
        test_parent_ele = ele[parent_mask(ele)]
        count_parent = count_obj(test_parent_ele)


        test_gen_mask = ele.matched_gen.distinctParent.pdgId == 24

        test_vertex_mask = ele.genPartFlav == 1

        test_ele = events.Electron

        test_kin_mask = gen_kinematic_mask(ele)

        test_kin_vertex = count_obj(ele[gen_kinematic_mask(ele) & primary_vertex_mask(ele)])
        test_kin_parent = count_obj(ele[gen_kinematic_mask(ele) & parent_mask(ele)])
        test_vertex_parent = count_obj(ele[primary_vertex_mask(ele) & parent_mask(ele)])

        test_all_ele = ele[gen_kinematic_mask(ele) & primary_vertex_mask(ele) & parent_mask(ele)]
        test_all = count_obj(test_all_ele)
        
        
        gold_ele = gold_cut(ele, jets)

        test_counting_None = ak.num([None, None, 3, 6, None, 7], axis=0)
        test_counting = ak.num([1, 2, 3, 6, 5, 7], axis=0)
        
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
                "filter_ele_count": filter_ele_count,
                "count_gen_kin": count_gen_kin,
                "count_primary_vertex": count_primary_vertex,
                "count_parent": count_parent,

                #"test_kin_vertex": test_kin_vertex,
                #"test_kin_parent": test_kin_parent,
                #"test_vertex_parent": test_vertex_parent,
                #"test_all": test_all,
                #"test_counting_None": test_counting_None,
                #"test_counting": test_counting,

                
                "test_gen_mask": test_gen_mask[30:40],
                "test_vertex_mask": test_vertex_mask[30:40],
                "test_ele": test_ele[30:40],
                "test_kin_mask": test_kin_mask,
                
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
                "test_gen_kinematic_ele": test_gen_kinematic_ele[:20],
                "test_primary_vertex_ele": test_primary_vertex_ele[:20],
                "test_parent_ele": test_parent_ele[:20],
                "test_all_ele": test_all_ele[:20],
                
                
            }
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
