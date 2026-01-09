"""
Code for preprocess LJSpeech Corpus:
https://keithito.com/LJ-Speech-Dataset/
"""

import glob
from tabnanny import verbose
from tokenize import Name
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
        json.dump({'filename': os.path.join(*dest.split('/')[3:]), 'text':[df['text']], 'original_data':df['original_data']}, f)

def split_all_audio_files(df, dest_root_path, max_workers=96):
    if not os.path.exists(dest_root_path):
        raise FileNotFoundError(f'Please Check {dest_root_path} exists')

    l = len(df)
    with tqdm.tqdm(total=l, desc=f'Processing {dest_root_path}') as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            threads = [executor.submit(convert_and_json_dump, row[0], os.path.join(dest_root_path, f'{i}.flac'), row, overwrite=False, verbose=False) for i, row in enumerate(df.iloc())]
            for _ in as_completed(threads):
                pbar.update(1)

def download_tsvs(urls:list, output_dir:str, extract:bool=False):
    os.makedirs(output_dir, exist_ok=True)
    for url in tqdm.tqdm(urls, desc="Downloading tsvs"):
        dest_path = os.path.join(output_dir, url.split("/")[-1])
        if os.path.isfile(dest_path):
            continue
        os.system(f'curl {url} --output {dest_path}')

        if extract:
            os.system(f'tar -xf {dest_path}')

def extract_covost_2_tsvs(tsv_tar_dir:str, dest:str, cv_tsv:str, version=2):
    extract_covost_2_tar_cmd = f'tar -xf {tsv_tar_dir} -C {dest}'
    os.system(extract_covost_2_tar_cmd)

    src_lang, tgt_lang = os.path.basename(tsv_tar_dir).split('.')[1].split('_')
    get_covost_splits_cmd = f'python /home/knoriy/fsx/raw_datasets/CoVoST_2/covost/get_covost_splits.py \
        --version {version} \
        --src-lang {src_lang} \
        --tgt-lang {tgt_lang} \
        --root {dest} \
        --cv-tsv {cv_tsv} \
        '
    os.system(get_covost_splits_cmd)

if __name__ == '__main__':
    import multiprocessing

    x_2_eng = [
        "https://dl.fbaipublicfiles.com/covost/covost_v2.fr_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.de_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.es_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.ca_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.it_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.ru_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.zh-CN_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.pt_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.fa_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.et_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.mn_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.nl_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.tr_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.ar_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.sv-SE_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.lv_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.sl_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.ta_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.ja_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.id_en.tsv.tar.gz",
        "https://dl.fbaipublicfiles.com/covost/covost_v2.cy_en.tsv.tar.gz",
    ]
    eng_2_x = [
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_de.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_ca.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_zh-CN.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_fa.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_et.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_mn.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_tr.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_ar.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_sv-SE.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_lv.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_sl.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_ta.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_ja.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_id.tsv.tar.gz',
        'https://dl.fbaipublicfiles.com/covost/covost_v2.en_cy.tsv.tar.gz',
    ]
    get_language_from_key = {
        'en':'english',
        'de':'german', 
        'fr':'french', 
        'nl':'dutch', 
        'ru':'russian', 
        'es':'spanish', 
        'it':'italian', 
        'tr':'turkish', 
        'fa':'persian',
        'ca':'catalan', 
        'zh-cn':'chinese', 
        'pt':'portuguese',
        'et':'estonian',
        'mn':'mongolian',
        'ar':'arabic',
        'sv-se':'swedish',
        'lv':'latvian',
        'sl':'slovenian',
        'ta':'tamil',
        'ja':'japanese',
        'id':'indonesian',
        'cy':'welsh',
        } 

    max_workers = multiprocessing.cpu_count()
    chunk = 512
    generate_subset_tsv = True

    root_path = '/home/knoriy/fsx/raw_datasets/CoVoST_2/'
    metadata_dir = "/home/knoriy/fsx/raw_datasets/CoVoST_2/"

    dataset_name = 'CoVoST_2'
    COMMON_VOICE_VERSION = 'cv-corpus-10.0-2022-07-04'

    s3 = fsspec.filesystem('s3')
    s3_dest = f's-laion/knoriy/{dataset_name}/{dataset_name}_tars/'

    download_tsvs(eng_2_x, os.path.join(root_path, 'tsvs/'))
    # download_tsvs(x_2_eng, "/home/knoriy/fsx/raw_datasets/CoVoST_2/tsvs")

    # uncomment to extract and create CoVoST tsvs
    # for tar in tqdm.tqdm(glob.glob(os.path.join(root_path, 'tsvs/**/*.tar.gz'), recursive=True), desc='Extracting tsvs'):
    #     extract_covost_2_tsvs(tar, os.path.join(root_path, 'tsvs/'), '/home/knoriy/fsx/raw_datasets/CoVoST_2/cv-corpus-10.0-2022-07-04/en/validated.tsv')

    # load metadata and configure audio paths
    tsvs = []
    for tsv in glob.glob(os.path.join(root_path, 'tsvs/**/*.tsv'), recursive=True):
        if any(word in os.path.basename(tsv) for word in ['test', 'train', 'dev']):
            tsvs.append(tsv)

    for tsv in tqdm.tqdm(tsvs, desc=f'processing:'):
        raw_df = pd.read_csv(tsv, sep='\t', on_bad_lines='skip')
        IS_TRAIN_VAL_OR_TEST, LANGUAGE = tsv.split('.')[-2], tsv.split('.')[-3]

        data = {}
        for row in raw_df.iloc():

            data.setdefault('paths', []).append(os.path.join(root_path, COMMON_VOICE_VERSION, LANGUAGE.split('_')[0], "clips", row['path']))
            data.setdefault('text', []).append(f"{row['translation']} translated to {get_language_from_key[LANGUAGE.split('_')[0]]}")
            data.setdefault('original_data', []).append(
                {
                    "sentence":row['sentence'],
                    "translation":row['translation'],
                    "client_id":row['client_id'],
                }
            )

        df = pd.DataFrame(data)
        
        dest_path = os.path.join(root_path.replace('raw_datasets', 'processed_datasets'), LANGUAGE, IS_TRAIN_VAL_OR_TEST, '')
        os.makedirs(dest_path, exist_ok=True)

        split_all_audio_files(df, dest_path)
        tardir(dest_path, dest_path, chunk, delete_file=True)

        # upload to s3 and delete local
        s3.put(dest_path, os.path.join(s3_dest, LANGUAGE, IS_TRAIN_VAL_OR_TEST)+'/', recursive=True)
        shutil.rmtree(dest_path)
