"""
Code for preprocess MusicNet dataset
"""

import os
from tqdm import tqdm
import pandas as pd
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

if __name__ == '__main__':
    data_dir = r'raw_datasets/musicnet'
    output_dir = 'processed_datasets/musicnet'

    # Make output directory.
    train_output_dir = os.path.join(output_dir, 'train')
    os.makedirs(train_output_dir, exist_ok=True)
    test_output_dir = os.path.join(output_dir, 'test')
    os.makedirs(test_output_dir, exist_ok=True)

    # Extract train data.
    file_id = 1
    for a in tqdm(os.listdir(os.path.join(data_dir, 'train_data')), total=len(os.listdir(os.path.join(data_dir, 'train_data')))):
        if a.endswith(".wav"):
            df = pd.read_csv(os.path.join(data_dir, 'train_labels', a.replace('.wav', '.csv')))
            audio_dict = df.to_dict(orient='list')
            audio_json = {"original_data": audio_dict}
            json_dump(audio_json, os.path.join(train_output_dir, f'{file_id}.json'))
            audio_to_flac(os.path.join(data_dir, 'train_data', a), os.path.join(train_output_dir, f'{file_id}.flac'))
            file_id += 1

    # Extract test data.
    for a in tqdm(os.listdir(os.path.join(data_dir, 'test_data')), total=len(os.listdir(os.path.join(data_dir, 'test_data')))):
        if a.endswith(".wav"):
            df = pd.read_csv(os.path.join(data_dir, 'test_labels', a.replace('.wav', '.csv')))
            audio_dict = df.to_dict(orient='list')
            audio_json = {"original_data": audio_dict}
            json_dump(audio_json, os.path.join(test_output_dir, f'{file_id}.json'))
            audio_to_flac(os.path.join(data_dir, 'test_data', a), os.path.join(test_output_dir, f'{file_id}.flac'))
            file_id += 1