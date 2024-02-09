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

import multiprocessing
from multiprocessing import Pool
from itertools import repeat


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.audio_utils import audio_to_flac
from utils.make_tar_utils import tardir

def convert_and_json_dump(df:pd.DataFrame, overwrite:bool=False, verbose:bool=False):
    dest = df['dest_path']
    file = df['src_path']

    if os.path.isfile(dest) and overwrite==False:
        print(f'{dest} already exists, skiping')
        return
    audio_to_flac(file, dest)
    with open(dest.replace('.flac', '.json'), 'w') as f:
        json.dump({'filename': os.path.join(*dest.split('/')[4:]), 'text':[df['WORD']], 'original_data':{'gender':df['GENDER'], 'language':dest.split('/')[-3]}}, f)

def split_all_audio_files(df, overwrite:bool=False, verbose:bool=False, chunksize:int=1):
    print(f'starting pool')
    with Pool() as pool:
        for result in tqdm.tqdm(pool.starmap(convert_and_json_dump, zip(df.iloc, repeat(overwrite), repeat(verbose)), chunksize=chunksize), total=len(df)):
            pass

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", help='Directory to the files to process, e.g. "/home/knoriy/fsx/raw_datasets/mswc/audio/fr.tar.gz" ', required=True)
    args = parser.parse_args()
    
    max_workers = multiprocessing.cpu_count()
    chunk = 512
    generate_subset_tsv = True

    root_path = '/fsx/knoriy/raw_datasets/mswc/'
    tar_dir = "/fsx/knoriy/raw_datasets/mswc/mswc.tar.gz"
    dataset_name = 'mswc'

    s3 = fsspec.filesystem('s3')
    s3_dest = f's-laion-audio/webdataset_tar/{dataset_name}/'

    language_tars_dirs = sorted(glob.glob(os.path.join(root_path, "audio/**.tar.gz")))
    if not language_tars_dirs:
        raise FileNotFoundError(f"Please check that the file have been extracted: {root_path}")

    dir = args.job

    with tarfile.open(dir, mode='r:gz') as mswc_audio:
        audio_path = os.path.split(dir)[0]
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
        # Convert to .flac
        dest_path  = splits_path.replace('.tar.gz', '/').replace('/raw_datasets/', '/processed_datasets/').replace('splits/', '')
        dest_path  = os.path.join(dest_path, train_test_dev)

        src_path = os.path.join(splits_path.replace('.tar.gz', '/').replace('splits/', 'audio/'), 'clips')
        os.makedirs(dest_path, exist_ok=True)
        os.makedirs(src_path, exist_ok=True)

        df = pd.read_csv(csv_path)
        df['dest_path'] = [os.path.join(dest_path, f'{i}.flac') for i, _ in enumerate(df.iloc())]
        df['src_path'] = [os.path.join(src_path, row['LINK']) for i, row in enumerate(df.iloc())]
        
        print("nan found", len(df[df.isna().any(axis=1)]))
        df = df.dropna()
        print("nan after drop:", len(df[df.isna().any(axis=1)]))

        split_all_audio_files(df, overwrite=True, chunksize=max_workers)

        tardir(dest_path, dest_path, chunk, delete_file=True)

        # upload to s3 and delete local
        s3.put(dest_path, os.path.join(s3_dest, os.path.basename(dir.split('.')[0]), train_test_dev), recursive=True)
        print('File Uploaded to: s3://', os.path.join(s3_dest, os.path.basename(dir.split('.')[0]), train_test_dev))
        shutil.rmtree(dest_path)

    # # clean extracted files
    # shutil.rmtree(splits_path.replace('splits/', 'audio/'))
    # shutil.rmtree(splits_path)