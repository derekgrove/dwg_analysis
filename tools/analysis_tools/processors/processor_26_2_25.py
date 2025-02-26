import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema
# my tools:
from analysis_tools.skimming.parent_filter import filter_cut
from analysis_tools.plotting.make_hist import make_1d_hist, make_2d_hist
from analysis_tools.skimming.ele_skim_v2 import (
#from analysis_tools.skimming.ele_skim_test import (
    count_obj,
    count_obj_events,
    count_obj_and_events,
    veto_minus_iso_hoe_cut,
    tight_minus_iso_hoe_cut,
    baseline_cut,
    baseline_plus_cut,
    bronze_cut,
    silver_cut,
    gold_cut,
)

#import hist
import dask
import hist.dask as dah


class MyProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        
        total_entries = ak.num(events, axis=0)
        
        ele = events.Electron
        total_ele = count_obj(ele)
        
        jets = events.Jet # need to give list of Jets to our bronze cuts for delta r matching:

        filtered_ele = filter_cut(ele)
        count_filtered_ele = count_obj(filtered_ele)

        ele=filtered_ele
        
        blp_ele = baseline_plus_cut(ele, jets)
        count_blp_ele = count_obj(blp_ele)
        
        gold_ele = gold_cut(ele, jets)
        count_gold_ele = count_obj(gold_ele)
        
        silver_ele = silver_cut(ele, jets)
        count_silver_ele = count_obj(silver_ele)
        
        bronze_ele = bronze_cut(ele, jets)
        count_bronze_ele = count_obj(bronze_ele)

        #(obj, attribute_a, binning_a, attribute_b, binning_b, label_a="axis_label_a", label_b="axis_label_b"):
        
        gold_hoe_pt_dist = make_2d_hist(gold_ele, "hoe", [60, 0, 1.2], "pt", [60, 5, 35], label_a = "hoe", label_b="pt")

        blp_hoe_pt_dist = make_2d_hist(blp_ele, "hoe", [60, 0, 1.2], "pt", [60, 5, 35], label_a = "hoe", label_b="pt")

        blp_mini_iso_pt_dist = make_2d_hist(blp_ele, "miniPFRelIso_all", [50, 0, 2], "pt", [90, 5, 50], label_a = "mini_iso", label_b="pt")

        gold_mini_iso_pt_dist = make_2d_hist(gold_ele, "miniPFRelIso_all", [50, 0, 2], "pt", [90, 5, 50], label_a = "mini_iso", label_b="pt")

        #(obj, attribute, binning, label="axis_label")
        gold_pt_dist = make_1d_hist(gold_ele, "pt", [45, 5, 50], label="gold pt")

        blp_pt_dist = make_1d_hist(blp_ele, "pt", [45, 5, 50],  label="blp pt")
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
                "total entries": total_entries,
                "total electrons": total_ele,
                "count_filtered_ele": count_filtered_ele,
                "count_blp_ele": count_blp_ele,
                "count_gold_ele": count_gold_ele,
                "count_silver_ele": count_silver_ele,
                "count_bronze_ele": count_bronze_ele,
                
                
            },

            "pt_binned": {

            },
        
            "calculations": {
                
            },
        
            "plots": {
                
                "gold_hoe_pt_dist": gold_hoe_pt_dist,
        
                "blp_hoe_pt_dist": blp_hoe_pt_dist,

                "blp_mini_iso_pt_dist": blp_mini_iso_pt_dist,

                "gold_mini_iso_pt_dist": gold_mini_iso_pt_dist,

                "gold_pt_dist": gold_pt_dist,

                "blp_pt_dist": blp_pt_dist,
                
                
            },
        
            "tests": {
                
            }
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
