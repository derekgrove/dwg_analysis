import json

# location of jsons:
# /home/cms-jovyan/dwg_analysis/src/dataset_tools

# this directory:
# /home/cms-jovyan/dwg_analysis/pikler

# datasets_master.json

relative_path = "../src/dataset_tools"
dataset_json = "datasets_master.json"

with open(relative_path+"/"+dataset_json) as file:
    master_datasets = json.load(file)


run_on = {}

for AOD_type in master_datasets.keys():
    print(AOD_type)
    run_on[AOD_type] = {}
    for year in master_datasets[AOD_type].keys():
        print(year)
        run_on[AOD_type][year] = {}
        for nickname in master_datasets[AOD_type][year].keys():
            print(nickname)
            run_on[AOD_type][year][nickname] = {} 
            
            run_on[AOD_type][year][nickname]['run'] = False #init all options to False
            run_on[AOD_type][year][nickname]['reduced_computation'] = True
            run_on[AOD_type][year][nickname]['use_client'] = False
            run_on[AOD_type][year][nickname]['num_chunks'] = 1
            run_on[AOD_type][year][nickname]['num_files'] = 1

# print(run_on.items())

with open("run_on.json", "w") as f:
    json.dump(run_on, f, indent=2)
