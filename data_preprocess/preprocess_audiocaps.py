"""
Code for preprocess BBCSoundEffects dataset:
https://sound-effects.bbcrewind.co.uk/
"""

import pandas as pd
import os
from tqdm import tqdm
import glob
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
import random

random.seed(1234)

if __name__ == '__main__':
    data_dir = r'/mnt/audio_clip/raw_datasets/audiocaps'
    output_dir = '/mnt/audio_clip/processed_datasets/audiocaps'

    if not os.path.exists(f'{data_dir}/train.csv'):
        os.system(f'wget https://raw.githubusercontent.com/cdjkim/audiocaps/master/dataset/train.csv -P {data_dir}')
        os.system(f'wget https://raw.githubusercontent.com/cdjkim/audiocaps/master/dataset/test.csv -P {data_dir}')
        os.system(f'wget https://raw.githubusercontent.com/cdjkim/audiocaps/master/dataset/val.csv -P {data_dir}')
        os.system(f'mv {data_dir}/val.csv {data_dir}/valid.csv')

    splits = ['train', 'valid', 'test']

    file_list = glob.glob(f'{data_dir}/**/*.wav', recursive=True)

    for split in splits:
        split_output_dir = os.path.join(output_dir, split)
        os.makedirs(split_output_dir, exist_ok=True)
        metadata = pd.read_csv(os.path.join(data_dir, split + '.csv'))
        for i, data in tqdm(metadata.iterrows(), total=len(metadata.index)):
            audio_file = os.path.join(data_dir, data['youtube_id'] + '.wav')
            text_file = audio_file.replace('.wav', '.txt')
            if os.path.exists(audio_file) and os.path.exists(text_file):
                audio_description = open(text_file).readlines()[0].strip()
                audio_save_path = os.path.join(split_output_dir, os.path.basename(audio_file).replace('.wav', '.flac'))
                audio_json = {'text': audio_description}
                audio_json_save_path = os.path.join(split_output_dir,
                                                    os.path.basename(audio_file).replace('.wav', '.json'))

                audio_to_flac(audio_file, audio_save_path, sample_rate=AUDIO_SAVE_SAMPLE_RATE)
                json_dump(audio_json, audio_json_save_path)
