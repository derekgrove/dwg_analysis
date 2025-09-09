import json
import argparse
import sys

#location of jsons:
#/home/cms-jovyan/dwg_analysis/src/dataset_tools

#this directory:
#/home/cms-jovyan/dwg_analysis/pikler

#datasets_master.json

relative_path = "../src/dataset_tools"
dataset_json = "datasets_master.json"

parser = argparse.ArgumentParser(
        description="Script to generate a run_on list (which needs further editing by user after generation)."
    )

parser.add_argument("--year", required=False, type=str)
parser.add_argument("--isMC", required=False, type=str)
parser.add_argument("--postBPix", required=False, type=str)
parser.add_argument("--custom_tag", required=False, type=str)
parser.add_argument("--AOD_version", required=False, type=str)

args = parser.parse_args()


arg_year        = args.year
arg_isMC        = args.isMC
arg_postBPix    = args.postBPix
arg_custom_tag  = args.custom_tag
arg_AOD_version = args.AOD_version

if arg_isMC is not None:
    arg_isMC = args.isMC.strip().lower()
    if arg_isMC in ['yes', 'true', 'y', 'oui']:
        arg_isMC = True
    elif arg_isMC in ['no', 'false', 'n', 'non']:
        arg_isMC = False
    else:
        sys.exit('postBPix entry unacceptable, must be "yes", or "no"')

if arg_postBPix is not None:
    arg_postBPix = args.postBPix.strip().lower()
    if arg_postBPix in ['yes', 'true', 'y', 'oui']:
        arg_postBPix = True
    elif arg_postBPix in ['no', 'false', 'n', 'non']:
        arg_postBPix = False
    else:
        sys.exit('postBPix entry unacceptable, must be "yes", or "no"')
        
with open(relative_path+"/"+dataset_json) as file:
    master_datasets = json.load(file)
    

run_on = {}

for AOD_type in master_datasets.keys():
    print(AOD_type)
    run_on[AOD_type] = {}
    for year in master_datasets[AOD_type].keys():
        if arg_year is not None and year != arg_year:
            continue
        print(year)
        run_on[AOD_type][year] = {}
        for nickname in master_datasets[AOD_type][year].keys():

            entry = master_datasets[AOD_type][year][nickname]

            # skip if filters don't match
            if arg_isMC is not None and entry["isMC"] != arg_isMC:
                continue
            if arg_postBPix is not None and entry["postBPix"] != arg_postBPix:
                continue
            if arg_AOD_version is not None and entry["AOD_version"] != arg_AOD_version:
                continue

            if arg_custom_tag is not None:
                tags = [t.strip() for t in entry.get("custom_tag", "").split(",")]
                if arg_custom_tag not in tags:
                    continue

            print(nickname)
            run_on[AOD_type][year][nickname] = {} 
            run_on[AOD_type][year][nickname]["run"] = False
            run_on[AOD_type][year][nickname]["reduced_computation"] = True
            run_on[AOD_type][year][nickname]["use_client"] = False
            run_on[AOD_type][year][nickname]["num_chunks"] = 1
            run_on[AOD_type][year][nickname]["num_files"] = 1


#print(run_on.items())

with open("run_on_custom.json", "w") as f:
    json.dump(run_on, f, indent=2)