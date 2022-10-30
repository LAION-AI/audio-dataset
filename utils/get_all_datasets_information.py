import os
import re
import json

def read_sizes_json(dic):
    values = dic.values()
    #sum up all the values
    return sum(values) 


os.system("aws s3 ls s3://s-laion-audio/webdataset_tar/ > temp.txxt")
folder_list = []
with open("temp.txxt", "r") as f:
    lines = f.readlines()
    for line in lines:
        # lines are like "                            PRE 130000_MIDI_SONGS/" 
        # we have to get the folder name:
        folder_name = re.findall(r"PRE (.*)/", line)[0]
        folder_list.append(folder_name)

numbers = {}


for folder_name in folder_list:
    # if "bbc" in folder_name.lower() \
    #     or "free" in folder_name.lower()\
    #     or "paramount" in folder_name.lower()\
    #     or "sonniss" in folder_name.lower()\
    #     or "we" in folder_name.lower()\
    #     or "stock" in folder_name.lower()\
    #     or "epidemic" in folder_name.lower()\
    #     or "clotho" in folder_name.lower()\
    #     or "audiocaps" in folder_name.lower()\
    #     or "audioset" in folder_name.lower()\
    #     or "wav" in folder_name.lower()\
    #     or "fsd" in folder_name.lower()\
    #     or "macs" in folder_name.lower():
    #     numbers[folder_name] = {}
    #     pass
    if "esc50" in folder_name.lower():
        numbers[folder_name] = {}
        pass
    else:
        continue

    os.system(f"aws s3 ls s3://s-laion-audio/webdataset_tar/{folder_name}/ > temp.txxt")
    splits = []
    with open("temp.txxt", "r") as f:
        lines = f.readlines()
        for line in lines:
            folder_name_list = re.findall(r"PRE (.*)/", line)
            if len(folder_name_list) < 1:
                continue
            split = folder_name_list[0]
            if split not in ["train", "valid", "test", "balanced_train", "unbalanced_train", "eval"]:
                continue
            splits.append(split)
    
    for split in splits:
        
        i = os.system(f"aws s3 cp s3://s-laion-audio/webdataset_tar/{folder_name}/{split}/sizes.json ./temp.txxt")
        if i != 0:
            continue
        with open("temp.txxt", "r") as f:
            dic = json.load(f)
            numbers[folder_name][split] = read_sizes_json(dic) 
            print("xgg")

# load the number dictionary as json file
with open("numbers.json", "w") as f:
    json.dump(numbers, f)

