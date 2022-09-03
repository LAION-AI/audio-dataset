"""
Code for preprocess MACS dataset.
"""

from tqdm import tqdm
import librosa
import os
import subprocess
import pandas as pd
import multiprocessing as mp
import time
import sys
import math
import re
import shutil
import zipfile
import yaml
import random
from split_and_rename import split_dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))



def process_data(meta, output_dir, audio_dir):
    from utils.file_utils import json_load, json_dump
    from utils.audio_utils import audio_to_flac
    from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
    import numpy as np
    file_id = 0
    for row in tqdm(meta.iterrows(), total=len(meta)):
        filename, annotations = row[1].values
        audio_path = audio_dir+'/'+filename
        ids, texts, tags = [], [], []
        for annotation in annotations:
            annotator_id, sentence, tags = annotation.values()
            tags.extend(tags)
            texts.append(sentence)

        tags = list(set(tags))
        texts = list(set(texts))
        original_data = {
                'title': 'MACS - Multi-Annotator Captioned Soundscapes',
                'description':"This is a dataset containing audio captions and corresponding audio tags for a number of 3930 audio files of the TAU Urban Acoustic Scenes 2019 development dataset (airport, public square, and park). The files were annotated using a web-based tool.",
                'license':'Other (Non-Commercial)',
                'filename':filename,
                'annotations':annotations
                }
        audio_json = {
                'text': texts, 
                'tag': tags, 
                'original_data':original_data,
                }

        audio_json_save_path = f'{output_dir}/{file_id}.json'
        audio_save_path = f'{output_dir}/{file_id}.flac'
        json_dump(audio_json, audio_json_save_path)
        audio_to_flac(audio_path, audio_save_path,
            AUDIO_SAVE_SAMPLE_RATE)
        file_id += 1

def process(dataset_name):
    output_dir = f'/home/ubuntu/marianna/clap/processed_datasets/{dataset_name}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio_dir = f'/home/ubuntu/marianna/clap/raw_datasets/MACS/AUDIO'
    meta_dir = f'/home/ubuntu/marianna/clap/raw_datasets/MACS/meta/MACS.yaml'

    with open(meta_dir) as f:
        meta = pd.DataFrame(yaml.safe_load(f)['files'])
    N = len(meta)

    file_id = 0
    num_process = 5
    processes = []
    out_dirs = [f'{output_dir}/{i} 'for i in range(num_process)]
    for out_dir in out_dirs:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
    rngs = [(i*int(N/num_process), (i+1)*int(N/num_process))
            for i in range(num_process)]
    print(rngs)
    s = time.time()
    for rng, out_dir in zip(rngs, out_dirs):
        start, end = rng
        p = mp.Process(target=process_data, args=[
                       meta.iloc[start:end], out_dir, audio_dir])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    e = time.time()
    print(f'Processed in {round(e-s, 2)} seconds')
    return output_dir


if __name__ == '__main__':
    from utils.merge_dirs import merge_dirs
    from utils.unzip import unzip_file
    dataset_name = 'MACS'
    process(dataset_name)