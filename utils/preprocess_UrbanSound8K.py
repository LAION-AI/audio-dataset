"""
Code for preprocess Urbansound8K dataset.
use condition: download UrbanSound8K.csv from https://zenodo.org/record/1203745#.Yt9TmXbMJhE and put it in the same folder as the script. 

Author: Yuchen Hui
"""

import pandas as pd
import os
from tqdm import tqdm
import sys

# this line is added to avoid "No module named 'utils' error"
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

id_to_class = {0: 'air conditioner', 1: 'car horn', 2: 'children playing', 3: 'dog bark', 4: 'drilling', 5: 'engine idling', 6: 'gun shot', 7: 'jackhammer', 8: 'siren', 9: 'street music'}

id_to_salience = {1: "foreground", 2: "background"}


def make_up_caption(class_label):
    '''
    make up caption from class label
    '''
    return "The sound of " + class_label + "."

if __name__ == '__main__':
    root_dir = r'/home/yuchen/raw/UrbanSound8K/'
    data_dir = os.path.join(root_dir, 'audio')
    metadata_dir = os.path.join(root_dir, 'metadata')
    output_dir = '/home/yuchen/processed/'

    # read csv
    # please use the UrbanSound8K.zip from s3://s-laion-audio/raw_dataset/
    # because the freesoundsource.csv is adapted by me(yuchen) a little bit.
    df8 = pd.read_csv(os.path.join(metadata_dir, 'UrbanSound8K.csv'), dtype= {'fsID': 'int'}) 
    df_author = pd.read_csv(os.path.join(root_dir, 'freesoundsource.csv'), dtype= {'soundid': 'int'})
    schema = zip(df8["slice_file_name"], df8["fsID"], df8["start"], df8["end"], df8["salience"], df8["fold"], df8["classID"])
    row_number = df8.shape[0]


    #total = 0
    for file_name, freesound_id, start, end, salience_id, fold, class_id in tqdm(schema, total=row_number):
        text = []
        tags = []
        original_data = {}

        class_label = id_to_class[int(class_id)]
        salience = id_to_salience[int(salience_id)]

        # determine tags
        tags.append(class_label)
        tags.append(salience)

        # determine text
        text.append(make_up_caption(class_label))

        # determine original data
        original_data["freesound_id"] = freesound_id
        original_data["start_time(in original recording)"] = start
        original_data["end_time"] = end
        original_data["salience"] = salience
        original_data["class_id"] = class_id
        original_data["file_name"] = file_name
        original_data["fold"] = fold
        original_data["author"] = df_author.query("soundid == @freesound_id").iloc[0]["author"]

        # determine input/output path
        audio_path = os.path.join(data_dir, f"fold{fold}/{file_name}")
        flac_file_name = file_name.replace(".wav", ".flac")
        audio_save_path = os.path.join(output_dir,flac_file_name)
        json_save_path = audio_save_path.replace('.flac', '.json')

        # convert audio to flac and save using ffmpeg
        audio_to_flac(audio_path, audio_save_path, sample_rate=AUDIO_SAVE_SAMPLE_RATE)

        # generate and save json file
        audio_json = {'text': text, 'tags': tags, 'original_data': original_data}
        json_dump(audio_json, json_save_path)

#        total += 1
#        if total > 10:
    #        break







