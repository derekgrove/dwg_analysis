import awkward as ak
from coffea import processor
from coffea.nanoevents import BaseSchema
import hist.dask as dah  # use eager version unless you're doing distributed work
import json
import sys
from pathlib import Path


current_dir = Path.cwd() #stupid that this is needed to ensure we import the correct .json while running from a different directory
src_dir = current_dir.parent / "src"
sys.path.append(str(src_dir))

from analysis_tools.taggers.lep_tagger_v3 import tag_ele_quality, tag_lpte_quality

from analysis_tools.taggers.gen_tagger import tag_gen_flags

from analysis_tools.taggers.lep_cuts import *

from analysis_tools.plotting import get_1d_pt_hist


class Processor(processor.ProcessorABC):
    def __init__(self):
        self.schema = BaseSchema

    def process(self, events):

        with open(f'{current_dir}/object_selections.json') as file:
            selections = json.load(file)
            print(selections)

        electron = events.Electron
        lpte = events.LowPtElectron
        
        electron = tag_ele_quality(electron)
        electron = tag_gen_flags(electron, ele_gen)
        lpte = tag_lpte_quality(lpte)
        lpte = tag_gen_flags(lpte, lpte_gen)

        pt_selected_electron = electron[electron.pt >= 7]
        pt_selected_lpte = lpte[lpte.pt < 7]

        ele = ak.concatenate([pt_selected_electron, pt_selected_lpte], axis=1)

        #with open("object_selection.json") as file:
        #    obj_sel = json.load(file)

        gen_categories = ["isSignal", "isLightFake", "isHeavyFake", "isTauFake"]

        quality_categories = ["isGold", "isSilver", "isBronze", "isGoldSilver"]

        plots = {
            "pt_hists": {},
            "eta_hists": {},
            "pt_eta_hists": {},
        }

        additional_masks = True #modify this to be whatever additional masks you want

        results = {}
        
        def basic_func_call_loop(obj, func, entry_name):
            
            for qual in qual_categories:
                print(qual)
                results[entry_name][qual] = {}
                qual_mask = getattr(ele, qual)
                for gen in gen_categories:
                    print(gen)
                    gen_mask = getattr(ele, gen)

                    sel_obj = obj[qual_mask & gen_mask & additional_masks]
                    
                    results[entry_name][qual][gen] = func(sel_obj)

            return results
        

        basic_fun_call_loop(ele, get_1d_pt_hist, "1d_pt_hist")
        
        output = {
            "total_entries": ak.num(events[events.run >= 0], axis=0),
            "plots": plots,
            "results": results,
        }

            
        return output

    def postprocess(self, accumulator):
        pass




