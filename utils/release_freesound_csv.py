import pandas
import os
import json
import glob
from tqdm import tqdm

def json_load(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

meta_paht = "/home/ubuntu/freesound_meta/freesound_parquet.parquet"

meta_df = pandas.read_parquet(meta_paht)
splits = [""]
root = "/mnt/freesound/split"
root  = "/mnt/freesound/old_freesound/split"

def generate_dict_for_csv(path):
    file_list = glob.glob(f'{path}/**/*.json', recursive=True)
    print("the number of json files is:", len(file_list))
    result_dict = {"url": [], "caption1": [], "caption2" : [], "freesound_id": []}
    for file in tqdm(file_list, total=len(file_list)):
        dic = json_load(file)
        captions = dic["text"]
        id = int(dic["original_data"]["id"])
        # find the entry with id = id in meta_df, get the downlaod_url
        download_url = meta_df[meta_df["id"] == id]["download_url"].values[0] 
        result_dict["url"].append(download_url)
        if len(captions) == 0:
            print("tnnd, zen me ken neng? jiu ni shi 0 a") 
            print("the bad file is:", file)
        if len(captions) == 1:
            result_dict["caption1"].append(captions[0])
            result_dict["caption2"].append("")
        if len (captions) == 2:
            result_dict["caption1"].append(captions[0])
            result_dict["caption2"].append(captions[1])
        if len(captions) > 2:
            print("pian ren shi ba")
            print("the bad file is:", file)

        result_dict["freesound_id"].append(id)
    return result_dict


for split in splits:
    root_split = os.path.join(root, split)
    ## get all .json files
    dic = generate_dict_for_csv(root_split)
    df = pandas.DataFrame(dic)
    #df.to_csv(f"/home/ubuntu/freesound_meta/freesound_no_overlap_all{split}.csv")
    df.to_csv(f"/home/ubuntu/freesound_meta/freesound_all{split}.csv")