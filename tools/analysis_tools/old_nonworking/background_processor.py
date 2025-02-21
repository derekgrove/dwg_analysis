import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema
# my tools:
from parent_filter import prim_ele
from skim import jet_cuts, lpte_cuts, ele_cuts


class SignalProcessor(processor.ProcessorABC):
    def __init__(self):
        self.schema = NanoAODSchema

    def process(self, events):
        
        dataset = events.metadata['dataset']
        total_entries = ak.num(events, axis=0)


        lpte = events.LowPtElectron
        ele = events.Electron
        count_lpte = ak.sum(ak.num(lpte))
        count_ele = ak.sum(ak.num(ele))
        muons = events.Muon
        jets = events.Jet # need to give list of Jets to our custodial cuts for delta r matching:

        e_count = ak.sum(ak.num(ele))
        lpte_count = ak.sum(ak.num(lpte))
        mu_count = ak.sum(ak.num(muons))

        # begin GenParent cuts:

        filtered_lpte = prim_ele(lpte)
        filtered_ele = prim_ele(ele)

        count_filtered_lpte = ak.sum(ak.num(filtered_lpte))
        count_filtered_ele = ak.sum(ak.num(filtered_ele))
        # begin custodial cuts:
        
        sel_lpte = filtered_lpte[lpte_cuts(filtered_lpte, jets)]
        sel_ele = filtered_ele[ele_cuts(filtered_ele, jets)]
        count_sel_lpte = ak.sum(ak.num(sel_lpte))
        count_sel_ele = ak.sum(ak.num(sel_ele))


        #background cut, first do an easy genflav == 0 cut:

        sel_lpte_gf0 = sel_lpte[sel_lpte.genPartFlav == 0]

        
        # "pt lists", used for making bins between each value to run over:
        
        lpte_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20]
        ele_pts = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 100]

        
        def calc_denom(background_obj, cut_list, pt_list):
            denom_dict = {}

                for pt_low, pt_high in zip(pt_list[:-1], pt_list[1:]):

                    denom_obj = background_obj[
                        (pt_low < signal_obj.pt) & 
                        (signal_obj.pt <= pt_high)
                    ]

                    # Count remaining objects
                    count = ak.sum(ak.num(num_obj))
                    denom_dict[(pt_low, pt_high)] = count

            return denom_dict  # Ensure return is outside the loop


        lpte_denom = calc_denom(sel_lpte_gf0, lpte_cut_list, lpte_pts)
        
        output = {
            "lpte_num": lpte_num,
            "total_entries": total_entries,
            "count_lpte": count_lpte,
            "count_filtered_lpte": count_filtered_lpte,
            "count_sel_lpte": count_sel_lpte,
            "count_ele": count_ele,
            "count_filtered_ele": count_filtered_ele,
            "count_sel_ele": count_sel_ele,
            
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass