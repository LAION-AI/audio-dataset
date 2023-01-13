import pandas
import os
import json
import glob
from tqdm import tqdm
from pathlib import Path

def json_load(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
meta_dir = f'/home/ubuntu/epidemic_meta/'

file_list = glob.glob(f"{meta_dir}/**/*.parquet", recursive=True)

# read all parquet files in file_list then combine them into one dataframe

def process_path(path):
    # read parquet file, get parquet file name and add it to the dataframe, 
    # return the new dataframe
    df = pandas.read_parquet(path)
    df["Class_name"] = Path(path).stem
    return df 

#df_list = p_map(process_path, file_list, num_cpus=8, desc="Reading parquet files")
df_list = list(map(process_path, file_list))
meta_df = pandas.concat([df for df in df_list], ignore_index=True)

splits = [""]
root = "/mnt/epidemic_sound_effects/epidemic_with_augmentation/split"

def generate_dict_for_csv(path):
    file_list = glob.glob(f'{path}/**/*.json', recursive=True)
    print("the number of json files is:", len(file_list))
    result_dict = {"url": [], "caption1": [], "caption2" : [], "caption_t5" : [], "epidemic_id": []}
    for file in tqdm(file_list, total=len(file_list)):
        dic = json_load(file)
        captions = dic["text"]
        id = int(dic["original_data"]["id"])

        # find the entry with id = id in meta_df, get the downlaod_url
        download_url = meta_df[abs(meta_df["id"] - id) < 0.001]["url"].values.tolist()
        if len(download_url) > 1:
            tr = download_url[0] == download_url[1]
            if tr:
                download_url = download_url[0]
            else:
                print("the different url")
                print("the bad file is:", file)
                exit(0)
        else:
            download_url = download_url[0]
        result_dict["url"].append(download_url)

        if len (captions) == 2:
            result_dict["caption1"].append(captions[0])
            result_dict["caption2"].append(captions[1])
        else:
            print("pian ren shi ba")
            print("the real length is:", len(captions))
            print("the bad file is:", file)

        t5_caption = dic["text_augment_t5"]
        if t5_caption is None:
            t5_caption = ""

        result_dict["caption_t5"].append(t5_caption)
        result_dict["epidemic_id"].append(id)
    return result_dict


for split in splits:
    root_split = os.path.join(root, split)
    ## get all .json files
    dic = generate_dict_for_csv(root_split)
    df = pandas.DataFrame(dic)
    df.to_csv(f"/home/ubuntu/epidemic_meta/Epidemic_all{split}.csv")