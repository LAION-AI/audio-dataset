import os
import json
import sys
import tqdm
import json
import pathlib
import fsspec
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from datasets import load_dataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.audio_utils import audio_to_flac
from utils.make_tar_utils import tardir


def get_json(file_path, class_metadata, ontology_dict, class_only=False):
    audio_id = os.path.basename(file_path).replace('.wav', '')
    class_labels = class_metadata[audio_id].replace('"', '').split(',')

    if class_only:
        class_names = [ontology_dict[c][0] for c in class_labels]
    else:
        class_names = [f"{ontology_dict[c][0]} ({ontology_dict[c][1]})" for c in class_labels]

    if len(class_names) > 1:
        text = "The sounds of " + ", ".join(class_names[:-1]) + " and " + class_names[-1]
    elif len(class_names) == 1:
        text = "The sound of " + class_names[0][0], class_names[0][1]
    else:
        raise ValueError("No class label found for audio id: {}".format(audio_id))

    json_data = {'text': text,
                 'original_data': {'class_labels': class_labels,
                                   'class_names': [ontology_dict[c][0] for c in class_labels], 
                                   'class_descriptions': [ontology_dict[c][1] for c in class_labels],
                                   }
                 }
    return json_data

def convert_and_json_dump(file:str, dest:str, df, class_metadata, ontology_dict, class_only=False, overwrite:bool=False):
    if os.path.isfile(dest) and os.path.isfile(dest.replace('.flac', '.json')) and not overwrite:
        print(f'{dest} already exists, skiping')
        return
    audio_to_flac(file, dest)


    get_json(file, class_metadata, ontology_dict, class_only=False)
    with open(dest.replace('.flac', '.json'), 'w') as f:
        m_dump = get_json(file, class_metadata, ontology_dict, class_only=False)
        m_dump['filename'] = os.path.join(*dest.split('/')[5:])
        json.dump(m_dump, f)


def split_all_audio_files(data, dest_root_path, ontology_dict, class_metadata, max_workers=96):
    if not os.path.exists(dest_root_path):
        raise FileNotFoundError(f'Please Check {dest_root_path} exists')

    l = len(data)
    with tqdm.tqdm(total=l, desc=f'Processing {dest_root_path}') as pbar:
        with ThreadPoolExecutor() as executor:
            threads = [executor.submit(convert_and_json_dump, row["audio"]["path"], os.path.join(dest_root_path, f'{i}.flac'), row, class_metadata, ontology_dict, False, False) for i, row in enumerate(data)]
            for _ in as_completed(threads):
                pbar.update(1)


def main():
    import multiprocessing
    max_workers = multiprocessing.cpu_count()

    ###############
    # Get metadata
    ###############
    
    #load ontology
    # !wget -O /tmp/ontology.json https://raw.githubusercontent.com/audioset/ontology/master/ontology.json

    with open('/tmp/ontology.json') as f:
        ontology = json.load(f)
        ontology_dict = {i['id']: (i['name'], i['description']) for i in ontology}

    #get and load CSV
    # !wget -O /tmp/eval_segments.csv http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/eval_segments.csv

    with open('/tmp/eval_segments.csv') as f:
        lines = f.readlines()
        lines = lines[3:]
        header_list = ['YTID', 'start_seconds', 'end_seconds', 'positive_labels']
        class_metadata = [l.strip().split(', ') for l in lines]
        class_metadata = pd.DataFrame(class_metadata, columns=header_list)
        class_metadata = dict(zip(class_metadata.YTID, class_metadata.positive_labels))

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

                split_all_audio_files(wikipedia_dataset, root_dest_path, ontology_dict, class_metadata, max_workers)
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
