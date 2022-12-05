"""
Code for preprocess freesound dataset.
"""
import pandas as pd
import os
from tqdm import tqdm
import sys
import re
import subprocess
import shlex
from p_tqdm import p_map
import traceback

# this line is added to avoid "No module named 'utils' error"
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
from utils.freesound_utils import get_id
from utils.freesound_utils import get_sampling_rate

if __name__ == '__main__':
    data_dir = r'/fsx/yuchen/freesound/'
    output_dir = r'/fsx/yuchen/processed_freesound/'
    metadata_file = r'/home/yuchen/raw/freesound/parquet/freesound_parquet.parquet'
    ignore_file = r'/home/yuchen/raw/freesound/filename_dic.txt'
    duration_file = r"/home/yuchen/raw/freesound/all_duration.txt" 

    blacklist = []
    ##step1: get ignore ids
    ##step2: read from freesound_parquet.parquet
    ##step3: 3min and 16khz
    ##step3: process ! 


    #-------------------------------------------------------------------------
    # read files    
    #-------------------------------------------------------------------------
    with open(ignore_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            ID = get_id(line)
            blacklist.append(ID)


    # >3min, discard.
    with open(duration_file, "r") as f:
        string_long = f.read()
        liste = re.findall(r"\(\'(.*?)\', ([0-9]*\.?[0-9]*)\)",string_long)
        for i in range (len(liste)):
            file_name = liste[i][0]
            duration = float(liste[i][1])
            threshold = 3*60
            if duration > threshold:
                blacklist.append(get_id(file_name))

    # read freesound_parquet.parquet
    df = pd.read_parquet(metadata_file)
    print(df.columns)
    #tuples = zip(df['id'], df['title'], df["tags:"],df["description"], df["username"], df["download_url"])

    #read data_dir 
    all_files = os.listdir(path = data_dir)
    print(len(all_files))

    # <16khz, discard.
    lq16hz = []
    def sampling_rate_ok(file_name):
        sampling_rate = get_sampling_rate(file_name)
        if sampling_rate == False:
            lq16hz.append(get_id(file_name))
            return
        if sampling_rate < 16000:
            lq16hz.append(get_id(file_name))
            with open(r'/home/yuchen/freesound_preprocess/lq16hz.txt', 'a') as f:
                f.write("sampling rate is: " + str(sampling_rate) + "\tand the file is: " + file_name +"\n")

    try:
        p_map(sampling_rate_ok, all_files, num_cpus = 32)
    except:
        with open(r"/home/yuchen/freesound_preprocess/preprocessing_error_log.txt", "a") as f:
            traceback.print_exc(file = f)
            exit()

    blacklist.extend(lq16hz)
    # save blacklist.
    with open("blacklist.txt", "a") as file:
        file.write(str(blacklist))
    print("lq16hz: ",len(lq16hz))
    print(len(set(blacklist)))

    # processing: filter html tags and _ and file extension,etc.
    # global variable 1: blacklist 2: df 3: all_files 
    def process(file_name):
        try:
            ID = get_id(file_name)
            if ID in blacklist:
                return
            json_dic = None 
            text = []
            tag = None 
            original_data = {}

            # path generation
            audio_path = os.path.join(data_dir, file_name) 
            audio_save_path = os.path.join(output_dir, str(ID)+".flac")
            json_save_path = audio_save_path.replace('.flac', '.json')

            df_temp = df[df['id'] == ID].head(1)
            tags = df_temp['tags:'].values[0]
            description = df_temp['description'].values[0]
            username = df_temp['username'].values[0]
            download_url = df_temp['download_url'].values[0]
            title = df_temp['title'].values[0]

            # split tags
            tags_raw_list = tags.split(",")
            tags_list = []
            for tag in tags_raw_list:
                if len(tag) > 0:
                    tags_list.append(tag)

            #original data generation:
            original_data['tags'] = tags_list
            original_data['description'] = description
            original_data['username'] = username
            original_data['download_url'] = download_url
            original_data['title'] = title
            original_data['id'] = int(ID)

            #"tag" generation
            tag = tags_list

            #"text" generation
            # process title:
            # 1. remove extension
            title = os.path.splitext(title)[0] 
            # 2. replace _ with space
            title = title.replace("_", " ")
            text.append(title + ".")

            # process description: 
            # 1. take first sentence
            description_list = description.split(".")
            # 2. if contains html tags, discard. 
            # html is context free, we simply can't use a regex to filter it, so I just use "<.*>".
            first_sentence = description_list[0]
            discard = False
            if "<" in first_sentence or ">" in first_sentence:
                discard = True
            if discard == False: 
                text.append(first_sentence + ".")

            # generate and save json file
            json_dic = {'text': text, 'tag': tag, 'original_data': original_data}
            json_dump(json_dic, json_save_path)

            #audio to flac and save using ffmpeg
            audio_to_flac(audio_path, audio_save_path, sample_rate=AUDIO_SAVE_SAMPLE_RATE)
        except:
            with open(r"/home/yuchen/freesound_preprocess/preprocessing_error_log.txt", "a") as f:
                f.write("the error file is:" + file_name + "\n")
                traceback.print_exc(file = f)

    p_map(process, all_files, num_cpus = 32)

