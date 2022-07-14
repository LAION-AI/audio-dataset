"""
Code for preprocess LJSpeech Corpus:
https://keithito.com/LJ-Speech-Dataset/
"""

import glob
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
        json.dump({'filename': os.path.join(*dest.split('/')[4:]), 'text':df['norm_text'], 'tag':{'raw_text':df['raw_text']}}, f)


def split_all_audio_files(df, dest_root_path, max_workers=96):
    if not os.path.exists(dest_root_path):
        raise FileNotFoundError(f'Please Check {dest_root_path} exists')

    l = len(df)
    with tqdm.tqdm(total=l, desc=f'Processing {dest_root_path}') as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            threads = [executor.submit(convert_and_json_dump, row[0], os.path.join(dest_root_path, f'{i}.flac'), row) for i, row in enumerate(df.iloc())]
            for _ in as_completed(threads):
                pbar.update(1)

def download_tsvs(urls:list, output_dir:str, extract:bool=False):
    os.makedirs(output_dir, exist_ok=True)
    for url in urls:
        dest_path = os.path.join(output_dir, url.split("/")[-1])
        if os.path.isfile(dest_path):
            continue
        os.system(f'curl {url} --output {dest_path}')

        if extract:
            os.system(f'tar -xf {dest_path}')

if __name__ == '__main__':
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
    download_tsvs(eng_2_x, "/home/knoriy/fsx/raw_datasets/CoVoST_2/tsvs/")
    download_tsvs(x_2_eng, "/home/knoriy/fsx/raw_datasets/CoVoST_2/tsvs")
    import multiprocessing

    max_workers = multiprocessing.cpu_count()
    chunk = 512
    generate_subset_tsv = True

    root_path = '/home/knoriy/datasets/raw_datasets/CoVoST_2/'
    metadata_dir = "/home/knoriy/datasets/raw_datasets/CoVoST_2/"

    dataset_name = 'CoVoST_2'

    s3 = fsspec.filesystem('s3')
    s3_dest = f's-laion/knoriy/{dataset_name}/{dataset_name}_tars/'

    # load metadata and configure audio paths
    df = pd.read_csv('/home/knoriy/fsx/raw_datasets/CoVoST_2/tsvs/covost_v2.en_de.dev.tsv', sep='\t')
    print(df.head())

    # create train, test, valid splits
    # train, test = train_test_split(df, test_size=0.2)
    # valid, test = train_test_split(test, test_size=0.2)
    # train_test_val = {'train/':train, 'test/':test, 'valid/':valid}


    # for key in tqdm.tqdm(train_test_val, desc=f'processing:'):
    #     df = train_test_val[key]
        
    #     dest_path = os.path.join(root_path.replace('raw_datasets', 'processed_datasets'),key )
    #     os.makedirs(dest_path, exist_ok=True)

    #     split_all_audio_files(df, dest_path)
    #     tardir(dest_path, dest_path, chunk, delete_file=True)

    #     # upload to s3 and delete local
    #     s3.put(dest_path, os.path.join(s3_dest, key), recursive=True)
    #     shutil.rmtree(dest_path)


    '''
        python get_covost_splits.py \
        --version 2 --src-lang en_de --tgt-lang <tgt_lang_code> \
        --root <root path to the translation TSV and output TSVs> \
        --cv-tsv <path to validated.tsv>
    '''