import awkward as ak
import numpy as np
from coffea import processor
from coffea.nanoevents import NanoAODSchema
# my tools:
from analysis_tools.parent_filter import prim_ele
from analysis_tools.ele_skim_old import custodial_cuts as ele_cust
from analysis_tools.ele_skim_old import jet_disambig as ele_disambig
from analysis_tools.ele_skim_old import bronze_cuts as ele_bronze
from analysis_tools.ele_skim_old import full_bronze_cuts as full_ele_bronze

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

        def count_events(ele_obj):
            sel_events = events[ak.num(ele_obj) >= 1]
            return ak.num(sel_events, axis=0)

        # begin GenParent cuts:

        filtered_ele = prim_ele(ele)
        filtered_ele = filtered_ele[filtered_ele.genPartFlav == 1]
        count_filtered_ele = ak.sum(ak.num(filtered_ele))
        events_filtered_ele = count_events(filtered_ele)

        
        
        # begin sequential custodial cuts:

        disambig_ele = filtered_ele[ele_disambig(filtered_ele, jets)]
        count_disambig_ele = ak.sum(ak.num(disambig_ele))
        events_disambig_ele = count_events(disambig_ele)


        #manually add the eta and cutBased cuts to disambig ele to get to custodial:
        cust_ele = disambig_ele[(np.abs(disambig_ele.eta) < 2.5) &  (disambig_ele.cutBased >= 2)]
        count_cust_ele = ak.sum(ak.num(cust_ele))
        events_cust_ele = count_events(cust_ele)
        
        #cust_ele = filtered_ele[ele_cust(filtered_ele)]
        #cust_ele = filtered_ele[ele_cust(filtered_ele)]
        #count_cust_ele = ak.sum(ak.num(cust_ele))

        vid_map = ele.vidNestedWPBitmap

        bronze_ele = cust_ele[ele_bronze(cust_ele)]
        count_bronze_ele = ak.sum(ak.num(bronze_ele))
        events_bronze_ele = count_events(bronze_ele)

        
        silver_ele = bronze_ele[(bronze_ele.sip3d > 2) & ((bronze_ele.miniPFRelIso_all * bronze_ele.pt) < 4) & ((bronze_ele.pfRelIso03_all * bronze_ele.pt) < 4) & (bronze_ele.mvaIso_WP80 == True)]
        count_silver_ele = ak.sum(ak.num(silver_ele))
        events_silver_ele = count_events(silver_ele)

        gold_ele = bronze_ele[(bronze_ele.sip3d < 2) & ((bronze_ele.miniPFRelIso_all * bronze_ele.pt) < 4) & ((bronze_ele.pfRelIso03_all * bronze_ele.pt) < 4) & (bronze_ele.mvaIso_WP80 == True)]
        count_gold_ele = ak.sum(ak.num(gold_ele))
        events_gold_ele = count_events(gold_ele)

        gold_ele_wo_iso = bronze_ele[(bronze_ele.sip3d < 2) & (bronze_ele.mvaIso_WP80 == True)]

        test_0 = ak.sum(ak.num(gold_ele_wo_iso))
        test_1 = (gold_ele_wo_iso.pt)
        test_2 = (gold_ele_wo_iso.miniPFRelIso_all)
        
        count_gold_ele = ak.sum(ak.num(gold_ele))
        events_gold_ele = count_events(gold_ele)

        # Create masks for gold and silver electrons
        gold_mask = (bronze_ele.sip3d < 2) & \
            ((bronze_ele.miniPFRelIso_all * bronze_ele.pt) < 4) & \
            ((bronze_ele.pfRelIso03_all * bronze_ele.pt) < 4) & \
            (bronze_ele.mvaIso_WP80 == True)

        silver_mask = (bronze_ele.sip3d > 2) & \
              ((bronze_ele.miniPFRelIso_all * bronze_ele.pt) < 4) & \
              ((bronze_ele.pfRelIso03_all * bronze_ele.pt) < 4) & \
              (bronze_ele.mvaIso_WP80 == True)

        # Exclude gold and silver electrons from bronze
        true_bronze_mask = ~(gold_mask | silver_mask)  # Keep only those NOT in gold or silver
        true_bronze_ele = bronze_ele[true_bronze_mask]
        
        # Count bronze-only electrons and events
        count_true_bronze_ele = ak.sum(ak.num(true_bronze_ele))
        events_true_bronze_ele = count_events(true_bronze_ele)
        
        # define histograms to fill:

        #hists of full distributions

        #no cuts:
        
        ele_mini_iso = dah.Hist.new.Regular(100, 0, 50, name = "mini_iso").Double()
        ele_mini_iso.fill(mini_iso = ak.flatten(ele.miniPFRelIso_all))

        ele_mini_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "mini_iso").Double()
        ele_mini_iso_zoom.fill(mini_iso = ak.flatten(ele.miniPFRelIso_all))
    
        ele_pfrel_iso = dah.Hist.new.Regular(100, 0, 50, name = "pfrel_iso").Double()
        ele_pfrel_iso.fill(pfrel_iso = ak.flatten(ele.pfRelIso03_all))

        ele_pfrel_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "pfrel_iso").Double()
        ele_pfrel_iso_zoom.fill(pfrel_iso = ak.flatten(ele.pfRelIso03_all))


        #primary electrons plots:

        filtered_ele_mini_iso = dah.Hist.new.Regular(100, 0, 50, name = "mini_iso").Double()
        filtered_ele_mini_iso.fill(mini_iso = ak.flatten(filtered_ele.miniPFRelIso_all))

        filtered_ele_mini_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "mini_iso").Double()
        filtered_ele_mini_iso_zoom.fill(mini_iso = ak.flatten(filtered_ele.miniPFRelIso_all))

        filtered_ele_pfrel_iso = dah.Hist.new.Regular(100, 0, 50, name = "pfrel_iso").Double()
        filtered_ele_pfrel_iso.fill(pfrel_iso = ak.flatten(filtered_ele.pfRelIso03_all))

        filtered_ele_pfrel_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "pfrel_iso").Double()
        filtered_ele_pfrel_iso_zoom.fill(pfrel_iso = ak.flatten(filtered_ele.pfRelIso03_all))

        #disambig cuts:

        disambig_ele_mini_iso = dah.Hist.new.Regular(100, 0, 50, name = "mini_iso").Double()
        disambig_ele_mini_iso.fill(mini_iso = ak.flatten(disambig_ele.miniPFRelIso_all))

        disambig_ele_mini_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "mini_iso").Double()
        disambig_ele_mini_iso_zoom.fill(mini_iso = ak.flatten(disambig_ele.miniPFRelIso_all))

        disambig_ele_pfrel_iso = dah.Hist.new.Regular(100, 0, 50, name = "pfrel_iso").Double()
        disambig_ele_pfrel_iso.fill(pfrel_iso = ak.flatten(disambig_ele.pfRelIso03_all))

        disambig_ele_pfrel_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "pfrel_iso").Double()
        disambig_ele_pfrel_iso_zoom.fill(pfrel_iso = ak.flatten(disambig_ele.pfRelIso03_all))

        #custodial cuts plots:

        cust_ele_mini_iso = dah.Hist.new.Regular(100, 0, 50, name = "mini_iso").Double()
        cust_ele_mini_iso.fill(mini_iso = ak.flatten(cust_ele.miniPFRelIso_all))

        cust_ele_mini_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "mini_iso").Double()
        cust_ele_mini_iso_zoom.fill(mini_iso = ak.flatten(cust_ele.miniPFRelIso_all))

        cust_ele_pfrel_iso = dah.Hist.new.Regular(100, 0, 50, name = "pfrel_iso").Double()
        cust_ele_pfrel_iso.fill(pfrel_iso = ak.flatten(cust_ele.pfRelIso03_all))

        cust_ele_pfrel_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "pfrel_iso").Double()
        cust_ele_pfrel_iso_zoom.fill(pfrel_iso = ak.flatten(cust_ele.pfRelIso03_all))
        
        #bronze_ele_mini_iso = Hist.new.Regular(100, 0 , 40, name = "mini_iso").Double()
        bronze_ele_mini_iso = dah.Hist.new.Regular(100, 0, 50, name="mini_iso").Double()
        bronze_ele_mini_iso.fill(mini_iso = ak.flatten(bronze_ele.miniPFRelIso_all))
        
        #zoom
        bronze_ele_mini_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_zoom.fill(mini_iso = ak.flatten(bronze_ele.miniPFRelIso_all))



        bronze_ele_pfrel_iso = dah.Hist.new.Regular(100, 0, 50, name = "pfrel_iso").Double()
        bronze_ele_pfrel_iso.fill(pfrel_iso = ak.flatten(bronze_ele.pfRelIso03_all))

        bronze_ele_pfrel_iso_zoom = dah.Hist.new.Regular(100, 0, 10, name = "pfrel_iso").Double()
        bronze_ele_pfrel_iso_zoom.fill(pfrel_iso = ak.flatten(bronze_ele.pfRelIso03_all))

        #zoomzoom

        bronze_ele_mini_iso_zoom_zoom = dah.Hist.new.Regular(100, 0, 2, name="mini_iso").Double()
        bronze_ele_mini_iso_zoom_zoom.fill(mini_iso = ak.flatten(bronze_ele.miniPFRelIso_all))

        bronze_ele_pfrel_iso_zoom_zoom = dah.Hist.new.Regular(100, 0, 2, name = "pfrel_iso").Double()
        bronze_ele_pfrel_iso_zoom_zoom.fill(pfrel_iso = ak.flatten(bronze_ele.pfRelIso03_all))

        #hists of iso * pt:
        
        bronze_ele_mini_iso_pt = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_pt.fill(mini_iso = ak.flatten(bronze_ele.miniPFRelIso_all * bronze_ele.pt))
        
        bronze_ele_pfrel_iso_pt = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_pfrel_iso_pt.fill(mini_iso = ak.flatten(bronze_ele.pfRelIso03_all * bronze_ele.pt))
        
        #pt bins 5 - 10

        bronze_ele_5_10 = bronze_ele[(bronze_ele.pt > 5) & (bronze_ele.pt <= 10)]
        
        bronze_ele_mini_iso_pt_5_10 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_pt_5_10.fill(mini_iso = ak.flatten(bronze_ele_5_10.miniPFRelIso_all * bronze_ele_5_10.pt))
        
        bronze_ele_pfrel_iso_pt_5_10 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_pfrel_iso_pt_5_10.fill(mini_iso = ak.flatten(bronze_ele_5_10.pfRelIso03_all * bronze_ele_5_10.pt))

        #pt bins 10 - 15

        bronze_ele_10_15 = bronze_ele[(bronze_ele.pt > 10) & (bronze_ele.pt <= 15)]
        
        bronze_ele_mini_iso_pt_10_15 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_pt_10_15.fill(mini_iso = ak.flatten(bronze_ele_10_15.miniPFRelIso_all * bronze_ele_10_15.pt))

        bronze_ele_pfrel_iso_pt_10_15 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_pfrel_iso_pt_10_15.fill(mini_iso = ak.flatten(bronze_ele_10_15.pfRelIso03_all * bronze_ele_10_15.pt))

        #pt bins 15 - 20

        bronze_ele_15_20 = bronze_ele[(bronze_ele.pt > 15) & (bronze_ele.pt <= 20)]
        
        bronze_ele_mini_iso_pt_15_20 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_pt_15_20.fill(mini_iso = ak.flatten(bronze_ele_15_20.miniPFRelIso_all * bronze_ele_15_20.pt))

        bronze_ele_pfrel_iso_pt_15_20 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_pfrel_iso_pt_15_20.fill(mini_iso = ak.flatten(bronze_ele_15_20.pfRelIso03_all * bronze_ele_15_20.pt))

#pt bins 20 - 25

        bronze_ele_20_25 = bronze_ele[(bronze_ele.pt > 20) & (bronze_ele.pt <= 25)]
        
        bronze_ele_mini_iso_pt_20_25 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_pt_20_25.fill(mini_iso = ak.flatten(bronze_ele_20_25.miniPFRelIso_all * bronze_ele_20_25.pt))

        bronze_ele_pfrel_iso_pt_20_25 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_pfrel_iso_pt_20_25.fill(mini_iso = ak.flatten(bronze_ele_20_25.pfRelIso03_all * bronze_ele_20_25.pt))

        #pt bins 25 - 30

        bronze_ele_25_30 = bronze_ele[(bronze_ele.pt > 25) & (bronze_ele.pt <= 30)]
        
        bronze_ele_mini_iso_pt_25_30 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_pt_25_30.fill(mini_iso = ak.flatten(bronze_ele_25_30.miniPFRelIso_all * bronze_ele_25_30.pt))

        bronze_ele_pfrel_iso_pt_25_30 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_pfrel_iso_pt_25_30.fill(mini_iso = ak.flatten(bronze_ele_25_30.pfRelIso03_all * bronze_ele_25_30.pt))

        #pt bins 30 - 40

        bronze_ele_30_40 = bronze_ele[(bronze_ele.pt > 30) & (bronze_ele.pt <= 40)]
        
        bronze_ele_mini_iso_pt_30_40 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_mini_iso_pt_30_40.fill(mini_iso = ak.flatten(bronze_ele_30_40.miniPFRelIso_all * bronze_ele_30_40.pt))

        bronze_ele_pfrel_iso_pt_30_40 = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        bronze_ele_pfrel_iso_pt_30_40.fill(mini_iso = ak.flatten(bronze_ele_30_40.pfRelIso03_all * bronze_ele_30_40.pt))

        gold_pt_mini_iso_dist = (
            dah.Hist.new
            .Regular(100, 0, 0.3, name="mini_iso")
            .Regular(100, 5, 30, name="pT")
        .Double()
        )

        gold_pt_pfrel_iso_dist = (
            dah.Hist.new
            .Regular(100, 0, 0.3, name="pfrel_iso")
            .Regular(100, 5, 30, name="pT")
        .Double()
        )


        gold_eta_mini_iso_dist = (
            dah.Hist.new
            .Regular(100, 0, 0.3, name="mini_iso")
            .Regular(100, -2.5, 2.5, name="eta")
        .Double()
        )
        
        gold_eta_pfrel_iso_dist = (
            dah.Hist.new
            .Regular(100, 0, 0.3, name="pfrel_iso")
            .Regular(100, -2.5, 2.5, name="eta")
        .Double()
        )
        
        gold_pt_mini_iso_dist.fill(pT=ak.flatten(gold_ele_wo_iso.pt), mini_iso=ak.flatten(gold_ele_wo_iso.miniPFRelIso_all))
        gold_pt_pfrel_iso_dist.fill(pT=ak.flatten(gold_ele_wo_iso.pt), pfrel_iso=ak.flatten(gold_ele_wo_iso.pfRelIso03_all))
        
        gold_eta_mini_iso_dist.fill(eta=ak.flatten(gold_ele_wo_iso.eta), mini_iso=ak.flatten(gold_ele_wo_iso.miniPFRelIso_all))
        gold_eta_pfrel_iso_dist.fill(eta=ak.flatten(gold_ele_wo_iso.eta), pfrel_iso=ak.flatten(gold_ele_wo_iso.pfRelIso03_all))
        
        gold_ele_pt = dah.Hist.new.Regular(100, 0, 60, name="pt").Double()
        gold_ele_pt.fill(pt=ak.flatten(gold_ele.pt))
        
        gold_ele_eta = dah.Hist.new.Regular(100, -3, 3, name="eta").Double()
        gold_ele_eta.fill(eta=ak.flatten(gold_ele.eta))
        
        gold_ele_sip3d = dah.Hist.new.Regular(100, 0, 10, name="sip3d").Double()
        gold_ele_sip3d.fill(sip3d=ak.flatten(gold_ele.sip3d))
        
        gold_ele_miniiso_pt = dah.Hist.new.Regular(100, 0, 10, name="mini_iso").Double()
        gold_ele_miniiso_pt.fill(ak.flatten(gold_ele.miniPFRelIso_all * gold_ele.pt))
        
        gold_ele_reliso_pt = dah.Hist.new.Regular(100, 0, 10, name="rel_iso").Double()
        gold_ele_reliso_pt.fill(ak.flatten(gold_ele.pfRelIso03_all * gold_ele.pt))

        gole_ele_cutbased = dah.Hist.new.Regular(100, 0, 10, name="cutbased").Double()
        gole_ele_cutbased.fill(ak.flatten(gold_ele.cutBased))

        #event_mask = ak.any(gold_ele, axis=1)  # True for events with at least one gold electron
        #gold_events = events[event_mask]
        #count_gold_events = ak.num(gold_events)
        

        
        # "pt lists", used for making bins between each value to run over:
        
        lpte_pts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20]
        ele_pts = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 100]

        # "cut lists", NanoAOD variable then the value to cut on:
        
        #lpte_cut_list = [("miniPFRelIso_all", 4)]
        ele_cut_list = [("pfRelIso03_all", 4), ("miniPFRelIso_all", 4)]

        
        def calc_num(signal_obj, cut_list, pt_list):
            numerator_dict = {}

            for cut, threshold in cut_list:
                numerator_dict[cut] = {}

                for pt_low, pt_high in zip(pt_list[:-1], pt_list[1:]):

                    num_obj = signal_obj[
                        (pt_low < signal_obj.pt) & 
                        (signal_obj.pt <= pt_high) & 
                        (getattr(signal_obj, cut) < threshold)  # Dynamically access the cut variable
                    ]

                    # Count remaining objects
                    count = ak.sum(ak.num(num_obj))
                    numerator_dict[cut][(pt_low, pt_high)] = count

            return numerator_dict  # Ensure return is outside the loop

        def effic_calc(signal_obj, pt_list):
            numerator_dict = {}
            
            for pt_low, pt_high in zip(pt_list[:-1], pt_list[1:]):

                num_obj = signal_obj[
                    (pt_low < signal_obj.pt) & 
                    (signal_obj.pt <= pt_high)
                ]

                # Count remaining objects
                count = ak.sum(ak.num(num_obj))
                numerator_dict[(pt_low, pt_high)] = count

            return numerator_dict  # Ensure return is outside the loop

        eff_numerator = effic_calc(gold_ele, ele_pts)
        
        ele_num = calc_num(bronze_ele, ele_cut_list, ele_pts)
        
        output = {
            "counts": {
                "total_entries": total_entries,
                "count_ele": count_ele,
                
                "count_filtered_ele": count_filtered_ele,
                "events_filtered_ele": events_filtered_ele,
                
                "count_disambig_ele": count_disambig_ele,
                "events_disambig_ele": events_disambig_ele,
                
                "count_cust_ele": count_cust_ele,
                "events_cust_ele": events_cust_ele,
                
                "count_bronze_ele": count_bronze_ele,
                "events_bronze_ele": events_bronze_ele,

                "count_silver_ele": count_silver_ele,
                "events_silver_ele": events_silver_ele,
                
                "count_gold_ele": count_gold_ele,
                "events_gold_ele": events_gold_ele,

                "count_true_bronze_ele": count_true_bronze_ele,
                "events_true_bronze_ele": events_true_bronze_ele,

                "test_0": test_0,
                "test_1": test_1,
                "test_2": test_2,
                
            },
        
            "calculations": {
                "ele_num": ele_num,
                "eff_numerator": eff_numerator,
            },
        
            "plots": {
                "ele_mini_iso": ele_mini_iso,
                "ele_mini_iso_zoom": ele_mini_iso_zoom,
                "ele_pfrel_iso": ele_pfrel_iso,
                "ele_pfrel_iso_zoom": ele_pfrel_iso_zoom,

                "filtered_ele_mini_iso": filtered_ele_mini_iso,
                "filtered_ele_mini_iso_zoom": filtered_ele_mini_iso_zoom,
                "filtered_ele_pfrel_iso": filtered_ele_pfrel_iso,
                "filtered_ele_pfrel_iso_zoom": filtered_ele_pfrel_iso_zoom,

                "disambig_ele_mini_iso": disambig_ele_mini_iso,
                "disambig_ele_mini_iso_zoom": disambig_ele_mini_iso_zoom,
                "disambig_ele_pfrel_iso": disambig_ele_pfrel_iso,
                "disambig_ele_pfrel_iso_zoom": disambig_ele_pfrel_iso_zoom,

                "cust_ele_mini_iso": cust_ele_mini_iso,
                "cust_ele_mini_iso_zoom": cust_ele_mini_iso_zoom,
                "cust_ele_pfrel_iso": cust_ele_pfrel_iso,
                "cust_ele_pfrel_iso_zoom": cust_ele_pfrel_iso_zoom,
                
                "bronze_ele_mini_iso": bronze_ele_mini_iso,
                "bronze_ele_mini_iso_zoom": bronze_ele_mini_iso_zoom,
                "bronze_ele_pfrel_iso": bronze_ele_pfrel_iso,
                "bronze_ele_pfrel_iso_zoom": bronze_ele_pfrel_iso_zoom,
                "bronze_ele_mini_iso_zoom_zoom": bronze_ele_mini_iso_zoom_zoom,
                "bronze_ele_pfrel_iso_zoom_zoom": bronze_ele_pfrel_iso_zoom_zoom,
                
                "bronze_ele_mini_iso_pt": bronze_ele_mini_iso_pt,
                "bronze_ele_pfrel_iso_pt": bronze_ele_pfrel_iso_pt,
                
                "bronze_ele_mini_iso_pt_5_10": bronze_ele_mini_iso_pt_5_10,
                "bronze_ele_pfrel_iso_pt_5_10": bronze_ele_pfrel_iso_pt_5_10,
                
                "bronze_ele_mini_iso_pt_10_15": bronze_ele_mini_iso_pt_10_15,
                "bronze_ele_pfrel_iso_pt_10_15": bronze_ele_pfrel_iso_pt_10_15,

                "bronze_ele_mini_iso_pt_15_20": bronze_ele_mini_iso_pt_15_20,
                "bronze_ele_pfrel_iso_pt_15_20": bronze_ele_pfrel_iso_pt_15_20,

                "bronze_ele_mini_iso_pt_20_25": bronze_ele_mini_iso_pt_20_25,
                "bronze_ele_pfrel_iso_pt_20_25": bronze_ele_pfrel_iso_pt_20_25,

                "bronze_ele_mini_iso_pt_25_30": bronze_ele_mini_iso_pt_25_30,
                "bronze_ele_pfrel_iso_pt_25_30": bronze_ele_pfrel_iso_pt_25_30,

                "bronze_ele_mini_iso_pt_30_40": bronze_ele_mini_iso_pt_30_40,
                "bronze_ele_pfrel_iso_pt_30_40": bronze_ele_pfrel_iso_pt_30_40,
                

                "gold_ele_pt": gold_ele_pt,
                "gold_ele_eta": gold_ele_eta,
                "gold_ele_sip3d": gold_ele_sip3d,
                "gold_ele_miniiso_pt": gold_ele_miniiso_pt,
                "gold_ele_reliso_pt": gold_ele_reliso_pt,
                "gole_ele_cutbased": gole_ele_cutbased,
                

                
                
                
                
            },
            
            "plots_2d": {
                "gold_pt_mini_iso_dist": gold_pt_mini_iso_dist,
                "gold_pt_pfrel_iso_dist": gold_pt_pfrel_iso_dist,
                "gold_eta_mini_iso_dist": gold_eta_mini_iso_dist,
                "gold_eta_pfrel_iso_dist": gold_eta_pfrel_iso_dist,
            },
        
            "tests": {
                #"count_gold_events": count_gold_events,
                "count_gold_ele": count_gold_ele,
                "count_silver_ele": count_silver_ele,
                "vid_map": vid_map,
                
            }  # Empty for now, but you can add test-related variables
        }
            
        return output
    
    def postprocess(self, accumulator):
        pass
        