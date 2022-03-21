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
    data_dir = r'/mnt/yusong_tianyu/raw_datasets/BBCSoundEffectsComplete/sounds'
    output_dir = '/mnt/yusong_tianyu/processed_dataset/BBCSoundEffects'
    test_portion = 0.1

    splits = ['train', 'test']

    file_list = glob.glob(f'{data_dir}/**/*.wav', recursive=True)
    random.shuffle(file_list)

    split_idx = int(np.round(len(file_list) * test_portion))
    test_list = file_list[:split_idx]
    train_list = file_list[split_idx:]
    split_file_list = {'train': train_list, 'test': test_list}

    for split in splits:
        for file in tqdm(split_file_list[split]):
            split_output_dir = os.path.join(output_dir, split)
            os.makedirs(split_output_dir, exist_ok=True)
            file_name = os.path.basename(file)
            audio_description = file_name[:-13]
            audio_save_path = os.path.join(split_output_dir, file_name.replace('.wav', '.flac'))
            audio_json = {'text': audio_description}
            audio_json_save_path = os.path.join(split_output_dir, file_name.replace('.wav', '.json'))

            audio_to_flac(file, audio_save_path, sample_rate=AUDIO_SAVE_SAMPLE_RATE)
            json_dump(audio_json, audio_json_save_path)
