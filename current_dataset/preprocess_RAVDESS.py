"""
Code for preprocess GigaSpeech Corpus:
https://github.com/SpeechColab/GigaSpeech
"""

import glob
import tqdm
import os
import glob
import pandas as pd
import sys
import tarfile
import json
import shutil
import fsspec

from sklearn.model_selection import train_test_split
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.audio_utils import audio_to_flac
from utils.make_tar_utils import tardir

def convert_and_json_dump(file:str, dest:str, df):
    audio_to_flac(file, dest, segment_start=df['begin_time'], segment_end=df['end_time'])
    with open(dest.replace('.flac', '.json'), 'w') as f:
        json.dump({'filename': os.path.join(*dest.split('/')[5:]), 'text':df['text'], 'tag':df['tag']}, f)


def split_all_audio_files(df, dest_root_path, max_workers=96):
    if not os.path.exists(dest_root_path):
        raise FileNotFoundError(f'Please Check {dest_root_path} exists')

    l = len(df)
    with tqdm.tqdm(total=l, desc=f'Processing {dest_root_path}') as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            threads = [executor.submit(convert_and_json_dump, row[0], os.path.join(dest_root_path, f'{i}.flac'), row) for i, row in enumerate(df.iloc())]
            for _ in as_completed(threads):
                pbar.update(1)

def create_df(root_path:str):
    wavs = glob.glob(root_path)
    return wavs


if __name__ == '__main__':
    import multiprocessing

    max_workers = multiprocessing.cpu_count()
    print("Num workers: ", max_workers)
    chunk = 512

    root_path = '/home/knoriy/fsx/raw_datasets/RAVDESS/ravdess/'
    metadata_dir = "/home/knoriy/fsx/raw_datasets/RAVDESS/ravdess/GigaSpeech.json"

    dataset_name = 'ravdess'

    s3 = fsspec.filesystem('s3')
    s3_dest = f's-laion/knoriy/RAVDESS/{dataset_name}_tars/'

    # load metadata and configure audio paths
    df = create_df(root_path)
    print(df)

    # # create train, test, valid splits
    # train, test = train_test_split(df, test_size=0.2)
    # valid, test = train_test_split(test, test_size=0.2)
    # train_test_val = {'train/':train, 'test/':test, 'valid/':valid}

    
    # for key in tqdm.tqdm(train_test_val, desc=f'processing:'):
    #     df = train_test_val[key]
        
    #     dest_path = os.path.join(root_path.replace('raw_datasets', 'processed_datasets'), key)
    #     os.makedirs(dest_path, exist_ok=True)

    #     split_all_audio_files(df, dest_path)
    #     tardir(dest_path, dest_path, chunk, delete_file=True)

    #     # upload to s3 and delete local
    #     s3.put(dest_path, os.path.join(s3_dest, key), recursive=True)
    #     shutil.rmtree(dest_path)