import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema
# my tools:
from analysis_tools.skimming.parent_filter import prim_ele
from analysis_tools.skimming.ele_skim_v2 import jet_disambig as ele_disambig
from analysis_tools.skimming.ele_skim_v2 import veto_minus_iso_cut as veto_minus_iso_cut
from analysis_tools.skimming.ele_skim_v2 import baseline_cut as baseline_cut
from analysis_tools.skimming.ele_skim_v2 import baseline_plus_cut as baseline_plus_cut
from analysis_tools.skimming.ele_skim_v2 import bronze_cut as bronze_cut
from analysis_tools.skimming.ele_skim_v2 import silver_cut as silver_cut
from analysis_tools.skimming.ele_skim_v2 import gold_cut as gold_cut
from analysis_tools.skimming.ele_skim_v2 import count_obj_events as count_obj_events
from analysis_tools.skimming.ele_skim_v2 import count_obj as count_obj
from analysis_tools.skimming.ele_skim_v2 import count_obj_and_events as count_obj_and_events
from analysis_tools.skimming.ele_skim_v2 import delta_r as delta_r
from analysis_tools.skimming.ele_skim_v2 import make_electron_histograms as make_electron_histograms
from analysis_tools.skimming.ele_skim_v2 import delta_r_electron_pairs as delta_r_electron_pairs



#import hist
import dask
import hist.dask as dah


class SignalProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        total_entries = ak.num(events, axis=0)
        
        ele = events.Electron
        ele=ele[(ele.pt > 10) & (ele.pt <= 20)]
        total_ele = count_obj(ele)

        
        jets = events.Jet # need to give list of Jets to our bronze cuts for delta r matching:

        dr_ele = delta_r(ele, ele)
        nonzero_dr = dr_ele[dr_ele != 0]  # Remove zeros (self-matching)
        min_dr_per_event = ak.min(nonzero_dr, axis=2)  # Smallest nonzero ΔR per event

        
        min_dr_dist = dah.Hist.new.Regular(100, 0, 1, name = "delta_R", growth = True).Double()
        #min_dr_dist.fill(delta_R=ak.flatten(min_dr_per_event))
        
        # begin GenParent filtering cuts: #######

        filtered_ele = prim_ele(ele)
        filtered_ele = filtered_ele[filtered_ele.genPartFlav == 1]
        
        count_filtered, events_filtered = count_obj_and_events(filtered_ele, events)

        # replace regular electron collection with genParent filtered and genFlav 1:
        
        ele = filtered_ele

        # begin baseline cuts: #######
        
        baseline_ele = baseline_cut(ele)
        count_baseline, events_baseline = count_obj_and_events(baseline_ele, events)

        
        # begin baseline+ cuts: #######

        blp_ele = baseline_plus_cut(ele, jets)
        count_blp, events_blp = count_obj_and_events(blp_ele, events)

        # begin bronze, silver, gold cuts: ######

        
        bronze_ele = bronze_cut(ele, jets)
        count_bronze, events_bronze = count_obj_and_events(bronze_ele, events)

        silver_ele = silver_cut(ele, jets)
        count_silver, events_silver = count_obj_and_events(silver_ele, events)

        gold_ele = gold_cut(ele, jets)
        count_gold, events_gold = count_obj_and_events(gold_ele, events)
        
        #make plots here:

        #we have these categories of electrons to make plots for:
        # filtered_ele, baseline_ele, baseline_plus_ele, bronze_ele, silver_ele, gold_ele

        filtered_plots = make_electron_histograms(filtered_ele, "filtered")

        baseline_plots = make_electron_histograms(baseline_ele, "baseline")

        blp_plots = make_electron_histograms(blp_ele, "blp")

        bronze_plots = make_electron_histograms(bronze_ele, "bronze")

        silver_plots = make_electron_histograms(silver_ele, "silver")

        gold_plots = make_electron_histograms(gold_ele, "gold")
        

        
        lpte_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20]
        ele_pts = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 100]

        # "cut lists", NanoAOD variable then the value to cut on:

        
        
        
        output = {
            "counts": {
                "total_entries": total_entries,
                "total_ele": total_ele,
                
                "events_filtered": events_filtered,
                "count_filtered": count_filtered,
                
                "events_baseline": events_baseline,
                "count_baseline": count_baseline,
                
                "events_blp": events_blp,
                "count_blp": count_blp,

                "events_bronze": events_bronze,
                "count_bronze": count_bronze,

                "events_silver": events_silver,
                "count_silver": count_silver,

                "events_gold": events_gold,
                "count_gold": count_gold,
                
            },

            "pt_binned": {

            },
        
            "calculations": {
                
            },
        
            "plots": {
                "filtered_plots": filtered_plots,
                "baseline_plots": baseline_plots,
                "blp_plots": blp_plots,
                "bronze_plots": bronze_plots,
                "silver_plots": silver_plots,
                "gold_plots": gold_plots,
                "min_dr_dist": min_dr_dist,
            
                
            },
        
            "tests": {
                "dr_ele": dr_ele,
                
            }
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
