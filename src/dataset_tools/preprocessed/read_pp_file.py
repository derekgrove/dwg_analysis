import gzip
import json

# Load the .json.gz file

def dump_file(str_filename):
    with gzip.open(str_filename, "rt") as f:
        data = json.load(f)
    
    # Dump it (pretty print)
    print(json.dumps(data, indent=2))