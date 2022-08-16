import os
from sre_parse import Verbose
import sys
import json
import tqdm
import pandas as pd
import pathlib
import fsspec
import shutil


from multiprocessing import Pool
from itertools import repeat
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.audio_utils import audio_to_flac
from utils.make_tar_utils import tardir


def convert_and_json_dump(df:pd.DataFrame, overwrite:bool=False, verbose:bool=False):
    dest = df['dest']
    file = df['path']

    os.makedirs(pathlib.Path(dest).parent, exist_ok=True)

    if os.path.isfile(dest) and overwrite==False:
        if verbose==True:
            print(f'{dest} already exists, skiping')
        return
    audio_to_flac(file, dest)
    with open(dest.replace('.flac', '.json'), 'w') as f:
        json.dump({'filename': os.path.join(*dest.split('/')[3:]), 'text':[df['text']], 'original_data':None}, f)
    return dest.replace('.flac', '.json')

def extract_tars(dir:pathlib.Path, dest:pathlib.Path):
    glob = dir.glob("**/*.tar.gz")

    for path in glob:
        path = pathlib.Path(path)
        tmp_dest = dest.joinpath(*(path.stem.split('_'))).with_suffix('')
        tmp_dest.mkdir(parents=True, exist_ok=True)
        cmd = f'tar -xf {path} -C {tmp_dest}'
        os.system(cmd)


def run_tasks(extract:bool=False, overwrite:bool=False, verbose:bool=False, chunksize:int=1):

    dataset_name = 'EmoV_DB'
    chunk = 512

    s3 = fsspec.filesystem('s3')
    s3_dest = pathlib.Path(f's-laion/knoriy/{dataset_name}/{dataset_name}_tars/')

    root_data_dir = pathlib.Path('/home/knoriy/fsx/raw_datasets/EmoV_db/')
    extracted_data_dir = pathlib.Path('/home/knoriy/fsx/raw_datasets/EmoV_db/raw/')
    if extract:
        extract_tars(root_data_dir, extracted_data_dir)
    
    raw_df = pd.read_csv(root_data_dir.joinpath('cmuarctic.csv'), sep="\t", header=None)

    glob = extracted_data_dir.glob('**/**/*.wav')
    train, test = train_test_split(list(glob), test_size=0.3)
    test, valid = train_test_split(list(test), test_size=0.3)
    train_test_valid = {'train':train, 'test':test, 'valid':valid}

    EmoV_DB_gender = {'sam':'male', 'jenie':'female', 'josh':'male', 'bea':'females'}

    for key in train_test_valid:
        dest_path = None
        df_data = []
        for i, path in enumerate(train_test_valid[key]):
            root_path = path.parents[0]
            file_name = path.name
            emotion = root_path.name
            actor = root_path.parents[0].name
            dest_path = str(path.parents[3].joinpath('EmoV_DB_tars', key)).replace('raw_datasets', 'processed_datasets')

            current_file = raw_df.loc[int(file_name.split('.')[0].split('_')[-1])-1]

            data = {}

            data['gender'] = EmoV_DB_gender[actor]
            data['emotion'] = emotion
            data['path'] = path
            data['dest'] = str(pathlib.Path(dest_path).joinpath(f'{i}.flac'))
            data['text'] = current_file[1]

            df_data.append(data)

        df = pd.DataFrame(df_data)

        print(f'starting pool for {key}')
        with Pool() as pool:
            for result in tqdm.tqdm(pool.starmap(convert_and_json_dump, zip(df.iloc, repeat(overwrite), repeat(verbose)), chunksize=chunksize), total=len(df_data)):
                pass

        tardir(dest_path, dest_path, chunk, delete_file=True)

        # upload to s3 and delete local
        s3.put(dest_path, s3_dest.joinpath(key), recursive=True)
        print('File Uploaded to: ', s3_dest.joinpath(key))
        shutil.rmtree(dest_path)
    
    # clean Extracted Files
    shutil.rmtree(extracted_data_dir)

if __name__ == '__main__':
    run_tasks(extract=True, chunksize=10)
