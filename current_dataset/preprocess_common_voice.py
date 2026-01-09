import os
import sys
import tqdm
import json
import pathlib
import fsspec
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import soundfile as sf
from datasets import load_dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from utils.audio_utils import audio_to_flac
from utils.make_tar_utils import tardir


def convert_and_json_dump(file:str, dest:str, df, overwrite:bool=False):
    if os.path.isfile(dest) and os.path.isfile(dest.replace('.flac', '.json')) and not overwrite:
        print(f'{dest} already exists, skiping')
        return
    
    sf.write(dest, df['audio']['array'], df['audio']['sampling_rate'])
    with open(dest.replace('.flac', '.json'), 'w') as f:
        json.dump({'filename': os.path.join(*dest.split('/')[5:]), 'text':[df['sentence']], 'original_data':{'up_votes':df['up_votes'], 'down_votes':df['down_votes'], 'age':df['age'], 'gender':df['gender'], 'accent':df['accent'], 'language':df['locale']}}, f)


def split_all_audio_files(data, dest_root_path, max_workers=96):
    if not os.path.exists(dest_root_path):
        raise FileNotFoundError(f'Please Check {dest_root_path} exists')

    l = len(data)
    with tqdm.tqdm(total=l, desc=f'Processing {dest_root_path}') as pbar:
        with ThreadPoolExecutor() as executor:
            threads = [executor.submit(convert_and_json_dump, row["audio"]["path"], os.path.join(dest_root_path, f'{i}.flac'), row, False) for i, row in enumerate(data)]
            for _ in as_completed(threads):
                pbar.update(1)



def main():
    import multiprocessing
    max_workers = multiprocessing.cpu_count()

    langs = ['ab', 'ar', 'en', 'fa', 'fr', 'es', 'sl', 'kab', 'cy', 'ca', 'de', 'tt', 'ta', 'ru', 'nl', 'it', 'eu', 'tr', 'zh-TW', 'br', 'pt', 'eo', 'zh-CN', 'id', 'ia', 'lv', 'ja', 'rw', 'sv-SE', 'cnh', 'et', 'ky', 'ro', 'hsb', 'el', 'cs', 'pl', 'rm-sursilv', 'rm-vallader', 'mn', 'zh-HK', 'cv', 'uk', 'mt', 'as', 'ka', 'fy-NL', 'dv', 'pa-IN', 'vi', 'or', 'ga-IE', 'fi', 'hu', 'th', 'lt', 'lg', 'hi', 'bas', 'sk', 'kmr', 'bg', 'kk', 'ba', 'gl', 'ug', 'hy-AM', 'be', 'ur', 'gn', 'sr', 'uz', 'mr', 'da', 'myv', 'nn-NO', 'ha', 'ckb', 'ml', 'mdf', 'sw', 'sat', 'tig', 'ig', 'nan-tw', 'mhr', 'bn', 'tok', 'yue', 'sah', 'mk', 'sc', 'skr', 'ti', 'mrj', 'tw', 'vot', 'az', 'ast', 'ne-NP']
    dataset_name = "common_voice_11_0"
    s3 = fsspec.filesystem('s3')

    with tqdm.tqdm(total=len(langs)) as pbar:
        for lang in langs:
            pbar.set_description(f'Prcessing {lang}')
            for split in ["train", "test", "validation"]:
                wikipedia_dataset = load_dataset(f"mozilla-foundation/{dataset_name}", lang, split=split)

                if split == "validation": split = "valid"
                root_dest_path = pathlib.Path(f"/fsx/knoriy/processed_datasets/{dataset_name}/{lang}/{split}/")
                root_dest_path.mkdir(parents=True, exist_ok=True)

                split_all_audio_files(wikipedia_dataset, root_dest_path, max_workers)
                tardir(str(root_dest_path), str(root_dest_path), 512, delete_file=False)

                # Upload only tar files to s3
                tar_files = (root_dest_path.glob('*.tar'))
                for tar in tar_files:
                    # upload to s3 and delete local
                    pbar.set_description(f'Prcessing {lang}: uploading {str(tar)} to s3')
                    s3_dest = f's-laion-audio/webdataset_tar/{dataset_name}/{lang}/{split}/{tar.name}'
                    s3.put(str(tar), s3_dest)
                # shutil.rmtree(root_dest_path)
                # break
            pbar.update(1)
            # break

if __name__ == '__main__':
    main()
