"""
Code for preprocess Multilingual Spoken Words Corpus:
https://mlcommons.org/en/multilingual-spoken-words/
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

from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.audio_utils import audio_to_flac
from utils.make_tar_utils import tardir

def convert_and_json_dump(file:str, dest:str, df):
    audio_to_flac(file, dest)
    with open(dest.replace('.flac', '.json'), 'w') as f:
        json.dump({'filename': os.path.join(*dest.split('/')[4:]), 'text':df['WORD'], 'tag':{'gender':df['GENDER'], 'language':dest.split('/')[-2]}}, f)


def split_all_audio_files(df, src_root_path, dest_root_path, max_workers=96):
    if not os.path.exists(dest_root_path):
        raise FileNotFoundError(f'Please Check {dest_root_path} exists')

    l = len(df)
    with tqdm.tqdm(total=l, desc=f'Processing {dest_root_path}') as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            threads = [executor.submit(convert_and_json_dump, os.path.join(src_root_path, row['LINK']), os.path.join(dest_root_path, f'{i}.flac'), row) for i, row in enumerate(df.iloc())]
            for _ in as_completed(threads):
                pbar.update(1)

if __name__ == '__main__':
    import multiprocessing
    
    max_workers = multiprocessing.cpu_count()
    chunk = 512
    generate_subset_tsv = True

    root_path = '/mnt/knoriy/raw_datasets/mswc/'
    tar_dir = "/mnt/knoriy/raw_datasets/mswc/mswc.tar.gz"
    dataset_name = 'mswc'

    s3 = fsspec.filesystem('s3')
    s3_dest = f's-laion/multilingual_spoken_words/{dataset_name}_tars/'

    language_tars_dirs = glob.glob(os.path.join(root_path, "audio/**.tar.gz"))

    for dir in language_tars_dirs:
        print(dir)
        audio_path = dir
        with tarfile.open(audio_path, mode='r:gz') as mswc_audio:
            audio_path = os.path.split(audio_path)[0]
            mswc_audio.extractall(audio_path)

        splits_path = dir.replace('audio', 'splits')
        with tarfile.open(splits_path, mode='r:gz') as mswc_split:
            splits_path = splits_path.replace('.tar.gz', '/')
            mswc_split.extractall(splits_path)

        tmp = glob.glob(os.path.join(splits_path, '**.csv'), recursive=True)
        csv_paths = []
        for csv_path in tmp:
            if '_splits.csv' not in csv_path:
                csv_paths.append(csv_path)

        for csv_path in csv_paths:
            if 'train' in csv_path:
                train_test_dev = 'train/'
            elif 'test' in csv_path:
                train_test_dev = 'test/'
            elif 'dev' in csv_path:
                train_test_dev = 'valid/'
            else:
                train_test_dev = 'other/'
            df = pd.read_csv(csv_path)

            # Convert to .flac
            dest_path  = splits_path.replace('.tar.gz', '/').replace('/raw_datasets/', '/processed_datasets/').replace('splits/', '')
            dest_path  = os.path.join(dest_path, train_test_dev)

            src_path = os.path.join(splits_path.replace('.tar.gz', '/').replace('splits/', 'audio/'), 'clips')
            os.makedirs(dest_path, exist_ok=True)
            os.makedirs(src_path, exist_ok=True)

            split_all_audio_files(df, src_path, dest_path, max_workers)

            tardir(dest_path, dest_path, chunk, delete_file=True)

            # upload to s3 and delete local
            s3.put(dest_path, os.path.join(s3_dest, os.path.basename(dir.split('.')[0]), train_test_dev), recursive=True)
            print('File Uploaded to: ', os.path.join(s3_dest, os.path.basename(dir.split('.')[0]), train_test_dev))
            shutil.rmtree(dest_path)

        # clean extracted files
        shutil.rmtree(splits_path.replace('splits/', 'audio/'))
        shutil.rmtree(splits_path)