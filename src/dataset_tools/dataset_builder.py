import json
import copy
import sys
from pathlib import Path

class basic_dataset_entry:
    
    def __init__(
        self,
        AOD_type,
        AOD_version,
        year,
        nickname,
        notes,
        MC,
        postBPix,
        custom_tag,
        branch,
        REMOTE_DIRECTORY,
        REDIRECTOR = "root://cms-xrd-global.cern.ch/",
    ):

        self.AOD_type = str(AOD_type).upper()
        self.AOD_version = str(AOD_version)
        self.year = str(year)
        self.nickname = str(nickname)
        self.notes = str(notes)
        self.MC = bool(MC)
        self.postBPix = bool(postBPix)
        self.custom_tag = str(custom_tag)
        self.branch = str(branch)
        self.REMOTE_DIRECTORY = str(REMOTE_DIRECTORY)
        self.REDIRECTOR = str(REDIRECTOR)
        

        if self.AOD_type not in ["AOD", "MINI", "NANO"]:
            print("AOD_type not acceptable, must be AOD, MINI, or NANO")
            sys.exit()

        if self.AOD_version not in ["9", "10", "11", "12", "13", "14"]:
            print("AOD_version not acceptable, must be between 9 and 14")
            sys.exit()
        
        if self.year not in ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]:
            print("year not acceptable, must be between 2016 and 2024.")
            sys.exit()

    
    def make_dict(self): #this is my v1 standard structure, please lets not fuck with this unless absolutely needed
        
        temp_dict = {
            self.AOD_type: {
                self.year: {
                    self.nickname:{
                        "notes": self.notes,
                        "isMC" : self.MC,
                        "postBPix": self.postBPix,
                        "custom_tag": self.custom_tag,
                        "AOD_version": self.AOD_version,
                        "branch": self.branch,
                        "REMOTE_DIRECTORY": self.REMOTE_DIRECTORY,
                        "REDIRECTOR": self.REDIRECTOR,
                        "numEvents": {},
                        "preprocessed_file": {}
                        
                    }
                }
            }
        }

        return temp_dict
        

    def append_to_master(self, path_to_master):
        
        temp_dict = self.make_dict()
        file_path = Path(path_to_master)
    
        if file_path.exists():
            with open(file_path, 'r') as file:
                data = json.load(file)
                backup = copy.deepcopy(data)

            if self.REMOTE_DIRECTORY in data:
                print("a link to this remote directory already exists in the loaded json, please check that you aren't overwriting things.")
                sys.exit()

            if (self.AOD_type in data and 
                self.year in data[self.AOD_type] and 
                self.nickname in data[self.AOD_type][self.year]):
        
                print("This entry (AOD_type, year, and nickname) is already present in .json, double check you're not accidentally adding a sample that already exists in the samples.")
                sys.exit()
    
            else:
                if self.AOD_type not in data:
                    data[self.AOD_type] = {}
                if self.year not in data[self.AOD_type]:
                    data[self.AOD_type][self.year] = {}
    
                

            
        else:
            print(f"File '{file_path}' does not exist, creating new .json")
            #sys.exit()
            with open(file_path, 'w') as file:
                json.dump(temp_dict, file, indent=4)
                return


        for aod_type, years in data.items():
            for year, nicknames in years.items():
                for nickname, entry in nicknames.items():
                    if entry.get("REMOTE_DIRECTORY") == self.REMOTE_DIRECTORY:
                        print(f"A link to this REMOTE_DIRECTORY already exists "
                              f"under {aod_type} -> {year} -> {nickname}.")
                        sys.exit()

        

        #finally, we can overwrite the old json with the new one:

        data[self.AOD_type][self.year][self.nickname] = temp_dict[self.AOD_type][self.year][self.nickname]

        # Create backup before modifying
        backup_path = Path(path_to_master.strip(".json")+"_before_last_update.json")
        with open(backup_path, 'w') as backup_file:
            json.dump(backup, backup_file, indent=4)
                    
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        print(f"Successfully added {self.nickname} to the master JSON file.")