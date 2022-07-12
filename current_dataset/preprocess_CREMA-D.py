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

def convert_and_json_dump(file:str, dest:str, df, overwrite:bool=False, verbose=False):
    if os.path.isfile(dest) and overwrite==False:
        if verbose==True:
            print(f'{dest} already exists, skiping')
        return
    audio_to_flac(file, dest)
    with open(dest.replace('.flac', '.json'), 'w') as f:
        json.dump({'filename': os.path.join(*dest.split('/')[5:]), 'text':df['text']}, f)


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
    wavs = glob.glob(os.path.join(root_path, '**/*.wav'), recursive=True)
    codes = {   'Statement':{   'IEO':"It's eleven o'clock", 
                                'TIE':"That is exactly what happened",
                                'IOM':"I'm on my way to the meeting",
                                'IWW':"I wonder what this is about",
                                'TAI':"The airplane is almost full",
                                'MTI':"Maybe tomorrow it will be cold",
                                'IWL':"I would like a new alarm clock",
                                'ITH':"I think I have a doctor's appointment",
                                'DFA':"Don't forget a jacket",
                                'ITS':"I think I've seen this before",
                                'TSI':"The surface is slick",
                                'WSI':"We'll stop in a couple of minutes",
                                },
                'Emotion':{     'ANG':'angery',
                                'DIS':'disgusted',
                                'FEA':'fearful',
                                'HAP':'happy',
                                'NEU':'neutral',
                                'SAD':'sad',
                        },
                'Emotional intensity':{ 'LO':'Low', 
                                        'MD':'Medium',
                                        'HI':'High',
                                        'XX':'Unspecified',
                                        },
                }
    demographics = pd.read_csv('/home/knoriy/fsx/raw_datasets/CREMA-D/VideoDemographics.csv', names=["ActorID","Age","Sex","Race","Ethnicity"])
    df_data = []
    for wav in tqdm.tqdm(wavs):
        file_name = os.path.basename(wav).split('.')[0]
        wav_codes = file_name.split('_')
        text_meta = [codes['Statement'][wav_codes[1]], codes['Emotion'][wav_codes[2]], codes['Emotional intensity'][wav_codes[3]]]
        demograpthics_meta = demographics.loc[demographics['ActorID'] == wav_codes[0]]

        male_or_female = 'woman' if demograpthics_meta["Sex"].values[0] == 'Female' else 'man'
        intensity = '' if text_meta[2] == 'Unspecified' else f'and {text_meta[2]} '
        text = f'A {male_or_female} saying "{text_meta[0]}" in a {text_meta[1]} {intensity}voice.'
        df_data.append({ 'path':wav, 'text':text})

    return pd.DataFrame(df_data)


if __name__ == '__main__':
    import multiprocessing

    max_workers = multiprocessing.cpu_count()
    print("Num workers: ", max_workers)
    chunk = 512

    root_path = '/home/knoriy/fsx/raw_datasets/CREMA-D/AudioWAV/'
    dataset_name = 'crema-d'

    s3 = fsspec.filesystem('s3')
    s3_dest = f's-laion/knoriy/RAVDESS/{dataset_name}_tars/'

    # load metadata and configure audio paths
    df = create_df(root_path)
    print(df.iloc()[1]['text'])

    # create train, test, valid splits
    train, test = train_test_split(df, test_size=0.2)
    valid, test = train_test_split(test, test_size=0.2)
    train_test_val = {'valid/':valid, 'train/':train, 'test/':test}

    
    for key in tqdm.tqdm(train_test_val, desc=f'processing:'):
        df = train_test_val[key]
        
        dest_path = os.path.join(root_path.replace('raw_datasets', 'processed_datasets').replace('AudioWAV/', ''), key)
        os.makedirs(dest_path, exist_ok=True)

        split_all_audio_files(df, dest_path)
        # tardir(dest_path, dest_path, chunk, delete_file=True)

        # # upload to s3 and delete local
        # s3.put(dest_path, os.path.join(s3_dest, key), recursive=True)
        # shutil.rmtree(dest_path)
        break