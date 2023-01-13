import pandas as pd
import os
import glob
from tqdm import tqdm
import json

def json_load(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

meta_path = "/home/ubuntu/audiostock_meta/audiostock_meta.parquet"

meta_df = pd.read_parquet(meta_path)
print(meta_df.columns)

json_path = "/mnt/audiostock/train/home"
file_list_1 = glob.glob(f'{json_path}/**/*.json', recursive=True)
json_path = "/mnt/audiostock/test/home"
file_list_2 = glob.glob(f'{json_path}/**/*.json', recursive=True)
file_list_1.extend(file_list_2 )

print("the number of json files is:", len(file_list_1))

result_dict = {"url": [], "caption": [] }

for file in tqdm(file_list_1):
    dic = json_load(file)
    caption = dic["text"][0]
    download_url = dic["original_data"]["URL"]
    result_dict["url"].append(download_url)
    result_dict["caption"].append(caption)

df = pd.DataFrame(result_dict)
df.to_csv(f"/home/ubuntu/audiostock_meta/audiostock_all.csv")

