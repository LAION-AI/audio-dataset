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
from multiprocessing import Pool

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.audio_utils import audio_to_flac
from utils.make_tar_utils import tardir

def convert_and_json_dump(file:str, dest:str, df, overwrite:bool=True, verbose=False):
    if os.path.isfile(dest) and overwrite==False:
        if verbose==True:
            print(f'{dest} already exists, skiping')
        return
    audio_to_flac(file, dest)
    with open(dest.replace('.flac', '.json'), 'w') as f:
        json.dump({'filename': os.path.join(*dest.split('/')[5:]), 'text':[df['text']], 'original_data':df['original_data']}, f)


def split_all_audio_files(df, dest_root_path, max_workers=96):
    if not os.path.exists(dest_root_path):
        raise FileNotFoundError(f'Please Check {dest_root_path} exists')

    l = len(df)
    with tqdm.tqdm(total=l, desc=f'Processing {dest_root_path}') as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            threads = [executor.submit(convert_and_json_dump, row[0], os.path.join(dest_root_path, f'{i}.flac'), row) for i, row in enumerate(df.iloc())]
            for _ in as_completed(threads):
                pbar.update(1)

def create_df(root_path:str, dataset_name:str=None):
    df = pd.read_csv(os.path.join(root_path, 'metadata.csv'), sep='|')

    df_data = []
    for row in df.iloc:
        path = os.path.join(root_path, row['audio_recording'].replace('wavs/', 'cleaned_webm/'))
        text = row['description'].format(user_id=f"A {row['gender']} in their {row['age']}", transcription=row['utterance'], emotion=row['emotion']) + f" Emotion intensity: {row['level']}."
        df_data.append({'path':path, 'text':text, 'original_data':{'age': row['age'], 'gender':row['gender'], 'emotion':row['emotion']}, 'transcript':row['utterance'], "level":row['level']})

    return pd.DataFrame(df_data)


if __name__ == '__main__':
    import multiprocessing

    max_workers = multiprocessing.cpu_count()
    print("Num workers: ", max_workers)
    chunk = 512

    root_path = '/admin/home-knoriy/DELETEME/EMNS/'
    dataset_name = 'EMNS'

    s3 = fsspec.filesystem('s3')
    s3_dest = f'laion-west-audio/webdataset_tar/{dataset_name}/'

    # load metadata and configure audio paths
    df = create_df(root_path)

    # create train, test, valid splits
    train, test = train_test_split(df, test_size=0.2)
    valid, test = train_test_split(test, test_size=0.2)
    train_test_val = {'valid/':valid, 'train/':train, 'test/':test}


    
    for key in tqdm.tqdm(train_test_val, desc=f'processing:'):
        df = train_test_val[key]
        
        dest_path = os.path.join(root_path.replace(dataset_name, f'{dataset_name}_processed'), key)
        os.makedirs(dest_path, exist_ok=True)

        split_all_audio_files(df, dest_path)
        tardir(dest_path, dest_path, chunk, delete_file=True)

        # upload to s3 and delete local
        # s3.put(dest_path, os.path.join(s3_dest, key), recursive=True)
        # shutil.rmtree(dest_path)