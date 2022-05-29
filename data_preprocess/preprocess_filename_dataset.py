"""
Code for preprocess filename dataset where the filename is the label (text description).
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
import argparse

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from functools import partial

executor = ProcessPoolExecutor(max_workers=cpu_count())

random.seed(1234)


def process_single_audio(file_path, json_data, output_dir):
    audio_id = os.path.basename(file_path).replace('.wav', '')
    json_dump(json_data, output_dir + '/' + audio_id + '.json')
    audio_to_flac(file_path, output_dir + '/' + audio_id + '.flac', sample_rate=AUDIO_SAVE_SAMPLE_RATE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default=None, help='data directory')
    parser.add_argument('--output_dir', type=str, default=None, help='dataset name')
    args = parser.parse_args()

    file_list = glob.glob(f'{args.data_dir}/**/*.wav', recursive=True)

    os.makedirs(args.output_dir, exist_ok=True)
    futures = []
    for file in tqdm(file_list):
        file_name = os.path.basename(file)
        audio_description = file_name.replace('.wav', '')
        audio_json = {'text': audio_description, 'original_data': {'file_path': file}}

        #process_single_audio(file, audio_json, args.output_dir)

        futures.append(executor.submit(partial(process_single_audio, file, audio_json, args.output_dir)))

    result = [future.result() for future in tqdm(futures)]
