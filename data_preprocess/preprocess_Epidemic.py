'''
Code for preprocess Epidemic_Sound dataset.
author:
Yuchen Hui 

'''
from p_tqdm import p_map 
from tqdm import tqdm
import os
import re
import sys
import glob 
import pandas as pd
import os
from pathlib import Path
#from keytotext import pipeline

# tests
# ls = ["wood", "fire", "large", "crackle", "wood fire crackle"]
# ls = ["household", "door", "creak", "squeak", "door", "creak", "squeaks", "whiny"]
# ls = ["foley", "door", "creak", "wood", "wood door creak", "squeak", "click"]
# nlp = pipeline("k2t")
# print(nlp(ls))
# nlp = pipeline("k2t-base")
# print(nlp(ls))
# nlp = pipeline("mrm8488/t5-base-finetuned-common_gen")
# print(nlp(ls))

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

cpu_num = os.cpu_count()-1
audio_dir = f'/mnt/epidemic_sound_effects/raw/'
meta_dir = f'/home/ubuntu/epidemic_meta/'
output_dir = f'/mnt/epidemic_sound_effects/processed/'

file_list = glob.glob(f"{meta_dir}/**/*.parquet", recursive=True)

# read all parquet files in file_list then combine them into one dataframe

def process_path(path):
    # read parquet file, get parquet file name and add it to the dataframe, 
    # return the new dataframe
    df = pd.read_parquet(path)
    df["Class_name"] = Path(path).stem
    return df 

#df_list = p_map(process_path, file_list, num_cpus=8, desc="Reading parquet files")
df_list = list(map(process_path, file_list))
df = pd.concat([df for df in df_list], ignore_index=True)

# change datatype of id to int
df["id"] = df["id"].astype(int)

# print dataframe title
# print(len(df))
# print(df.columns)
# print the "Class_name" column
# print(df["Class_name"].unique())

# download audio files from "url" column of dataframe using wget, 
# replace the file name as "id" column of dataframe, 
# without touching the extension. 
tuples = zip(df["url"], df["id"])

def download_audio(tuple):
    url, id = tuple
    root_ext = os.path.splitext(url)
    ext = root_ext[1]            # ext = .mp3 
    file_name = str(id) + ext
    file_path = os.path.join(audio_dir, file_name)
    os.system(f"wget {url} -O {file_path}")

#p_map(download_audio, tuples, num_cpus=cpu_num, desc="Downloading audio files")

# procssing function
# read all columns of dataframe ('title', 'id', 'added', 'length', 'bpm', 
# 'isSfx', 'hasVocals','energyLevel', 'genres', 'url', 
# 'metadataTags','Class_name') into zip
big_tuples = zip(df["title"], 
                df["id"], 
                df["added"], 
                df["length"], 
                df["bpm"], 
                df["isSfx"], 
                df["hasVocals"], 
                df["energyLevel"], 
                df["genres"], 
                df["url"], 
                df["metadataTags"], 
                df["Class_name"])

# "id" "genre" "title" "metadataTags","url", "Class_name"

# key to text
#nlp = pipeline("mrm8488/t5-base-finetuned-common_gen")

def process(tuples):
    title, id, added, length, bpm, isSfx, hasVocals, energyLevel, genres, url, metadataTags, Class_name = tuples

    # json file generation

    # process the title: remove the space and number at the end of the title
    title = re.sub(r'\d+$', '', title).strip()
    #print("the title is", title)

    # process the metadataTags: use keytotext to make a caption using metadataTags
    #made_up_caption = nlp(metadataTags)
    #print("the made up caption is", made_up_caption)

    # 2nd way of processing metadataTags: "the sounds of tag1, tag2, tag3... "
    made_up_caption_2 = "the sounds of " + ", ".join(metadataTags[:-1]) + ", and " + metadataTags[-1] + "."


    # determine the "text" entry of the json file
    text = [title,made_up_caption_2]
    #print("the text is", text)
    # determine the "tag" entry of the json file
    tag = [Class_name, genres] 
    tag.extend(metadataTags)
    #print("the tag is", tag)

    # determine the "original_data" entry of the json file
    original_data = {
        "title": title,
        "id": id, 
        "added": added, 
        "length": length, 
        "bpm": bpm, 
        "isSfx": isSfx, 
        "hasVocals": hasVocals, 
        "energyLevel": energyLevel, 
        "genres": genres, 
        "url": url, 
        "metadataTags": metadataTags.tolist(), 
        "Class_name": Class_name}
    #print("the original_data is", original_data)
    # json file content
    json_dic = {"text" : text, "tag" : tag, "original_data" : original_data}

    # reget the file name
    root_ext = os.path.splitext(url)
    ext = root_ext[1]            # ext = .mp3 
    filename = str(id) + ext

    # determine input/output path
    audio_path = os.path.join(audio_dir, filename)
    flac_file_name = filename.replace(ext, ".flac")
    audio_save_path = os.path.join(output_dir,flac_file_name)
    json_save_path = audio_save_path.replace('.flac', '.json')

    # convert audio to flac
    audio_to_flac(audio_path, audio_save_path, AUDIO_SAVE_SAMPLE_RATE) 

    # save json
    json_dump(json_dic, json_save_path)

if __name__ == '__main__':
    n = 0
    # for bit_tuples in tqdm(big_tuples, desc="Processing audio files"):
    #     process(bit_tuples)
    #     n+=1
    #     if n == 11:
    #         break
    p_map(process, big_tuples, num_cpus=12, desc="Processing audio files")
    




