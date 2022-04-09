"""
Code for preprocess Clotho dataset:
https://zenodo.org/record/4783391#.YgdAa9-ZNPY
"""

import pandas as pd
import os
from tqdm import tqdm
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

if __name__ == '__main__':
    data_dir = r'/mnt/audio_clip/raw_datasets/Clotho'
    output_dir = '/mnt/audio_clip/processed_datasets/Clotho'

    splits = ['development', 'evaluation', 'validation']

    # transfer "development, evaluation, validation" to "train, test, valid".
    split_output_name_dict = {
        'development': 'train',
        'evaluation': 'valid',
        'validation': 'test'
    }

    for split in splits:
        split_output_dir = os.path.join(output_dir, split_output_name_dict[split])
        os.makedirs(split_output_dir, exist_ok=True)
        caption_data = pd.read_csv(
            os.path.join(data_dir, f'clotho_captions_{split}.csv'))
        for i, data in tqdm(caption_data.iterrows(), total=len(caption_data.index)):
            audio_path = os.path.join(data_dir, split, data.file_name)
            audio_caption = [data[f'caption_{i}'] for i in range(1, 6)]
            audio_save_path = os.path.join(split_output_dir,
                                           data.file_name.replace('.wav', '.flac'))
            audio_json = {'text': audio_caption}
            audio_json_save_path = os.path.join(
                split_output_dir, data.file_name.replace('.wav', '.json'))

            audio_to_flac(audio_path, audio_save_path,
                          sample_rate=AUDIO_SAVE_SAMPLE_RATE)
            json_dump(audio_json, audio_json_save_path)
