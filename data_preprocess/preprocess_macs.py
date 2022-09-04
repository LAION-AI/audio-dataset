"""
Code for preprocess MACS dataset.
"""
import yaml
from pathlib import Path
import pandas as pd
import multiprocessing as mp

from utils.file_utils import json_load, json_dump
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
from utils.audio_utils import audio_to_flac

def process_data(file_id, meta):

    audio_path = data_dir / "TAU-urban-acoustic-scenes-2019-development" / "audio" / meta['files']["filename"]
    
    # Check if the file exists
    assert audio_path.is_file()
    
    audio_json = {
    "text": None,
    "tag": None, 
    "original_data": {
        "title": "MACS - Multi-Annotator Captioned Soundscapes", 
        "description": "This is a dataset containing audio captions and corresponding audio tags for a number of 3930 audio files of the TAU Urban Acoustic Scenes 2019 development dataset (airport, public square, and park). The files were annotated using a web-based tool.", 
        "license": "Other (Non-Commercial)",
        "filename": None,
        "annotations": None
        }
    }
    
    texts = []
    tags = []
    for i in meta["files"]["annotations"]:
        texts.append(i["sentence"])
        tags.extend(i["tags"])
    
    audio_json["original_data"]["filename"] = meta['files']["filename"]
    audio_json["original_data"]["annotations"] = meta['files']["annotations"]
    
    audio_json["text"] = texts
    audio_json["tag"] = tags

    audio_json_save_path = output_dir/f"{file_id}.json"
    audio_save_path = output_dir/f"{file_id}.flac"
    
    json_dump(audio_json, audio_json_save_path)
    audio_to_flac(audio_path, audio_save_path, AUDIO_SAVE_SAMPLE_RATE)


if __name__ == '__main__':
    data_dir = Path('/fsx/MACS/TAU2019')
    output_dir = Path('/fsx/MACS/processed_datasets')

    meta_dir = data_dir/ "MACS.yaml"

    with open(meta_dir) as f:
        meta = pd.DataFrame(yaml.safe_load(f))

    meta_dict = meta.to_dict(orient='index')

    for i in meta_dict:
        p = mp.Process(target=process_data, args=(i, meta_dict[i]))
