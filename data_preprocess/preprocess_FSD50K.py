"""
Code for preprocess FSD50K dataset.
use condition: download ontology.json from https://github.com/audioset/ontology/blob/master/ontology.json, and put it in the parent folder of FSD50K.dev_audio
"""

from unicodedata import name
import pandas as pd
import os
from tqdm import tqdm
import sys

# this line is added to avoid "No module named 'utils' error"
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE


if __name__ == '__main__':
    data_dir = r'/mnt/yuchenXi/raw_datasets/FSD50K'
    output_dir = '/mnt/audio_clip/processed_datasets/FSD50K'


    #-------------------------------------------------------------------------
    # read ontology.json    
    #-------------------------------------------------------------------------
    ontology_info_list = json_load(os.path.join(data_dir, 'ontology.json'))
        #convert ontology to a dict (instead of a list of dicts)
    ontology = {dict["id"] : dict["name"].split(", ") for dict in ontology_info_list} 

    # counter for file name
    # make output directories
    splits = ['train', 'valid', 'test']
    for split in splits:
        split_output_dir = os.path.join(output_dir, split)
        os.makedirs(split_output_dir, exist_ok=True)


    # The game, Mrs hudson, is on.
    # type can be dev or eval
    def process(type):
        file_id = 1

        #-------------------------------------------------------------------------
        # read files according to type                                          
        #-------------------------------------------------------------------------
        # json
        info_dict = json_load(os.path.join(data_dir, f'FSD50K.metadata/{type}_clips_info_FSD50K.json'))
        # ground truth
        ground_truth_df = pd.read_csv(os.path.join(data_dir, f'FSD50K.ground_truth/{type}.csv'))
        # uniform dataframe for dev and eval..
        if ground_truth_df.shape[1] == 3:
            ground_truth_df.insert(loc = 3, column = "split", value = 0)
        # collection
        collection_df = pd.read_csv(os.path.join(data_dir, f'FSD50K.metadata/collection/collection_{type}.csv'))

        liste = zip(ground_truth_df["fname"],
                ground_truth_df["mids"],
                ground_truth_df["split"],
                collection_df["mids"])          # liste = list in french

        for fname, mids, split_suggestion,collection_mids in tqdm(liste, total = len(liste)):
            
            # int --> str
            fname = str(fname)

            # determine input/output path
            audio_path = os.path.join(data_dir, f"FSD50K.{type}_audio", f"{fname}.wav")
            if type == "eval":
                audio_save_path = os.path.join(output_dir, "test", f"{file_id}.flac")
            elif split_suggestion == "train":
                audio_save_path = os.path.join(output_dir, "train", f"{file_id}.flac")
            elif split_suggestion == "val":
                audio_save_path = os.path.join(output_dir, "valid", f"{file_id}.flac")
            json_save_path = audio_save_path.replace('.flac', '.json')
            

            # convert audio to flac and save using ffmpeg
            audio_to_flac(audio_path, audio_save_path, sample_rate=AUDIO_SAVE_SAMPLE_RATE)

            # retrive informations from 4 files
            #   1. dev/eval.csv 2. collection_dev/eval.csv 3. ontology.json 4. dev/eval_clips_info_FSD50K.json 
            '''
            text: made-up description by class lables
            tags: class labels and tags in metadata (dev/eval_clips_info_FSD50K.json)
            original_data: fname, mids, (title, description,liscens, uploader)
            (in dev/eval_clips_info_FSD50K.json)
            '''
            text = []
            tags = []
            original_data = []; 

            metadata = info_dict[fname]

            #determine mids
            if len(str(collection_mids)) < 5:   
                # if collection_mids is empty, pandas will read 0, i.e. a float
                pass
            else:
                mid_set = set(mids.split(',')).union(set(collection_mids.split(',')))

            #determine class labels
            for mid in mid_set:
                tags.extend(ontology[mid])
            class_lables_list = tags.copy()

            #determine text
            sentence = "The sounds of "
            for i in range(len(class_lables_list)): 
                if i < len(class_lables_list) - 2:
                    sentence += class_lables_list[i] + ", "
                elif i == len(class_lables_list) - 2:
                    sentence += class_lables_list[i] + " and "
                else:
                    sentence += class_lables_list[i]
            text.append(sentence)

            #determine tags
            tags = list(set(tags).union(set(map(lambda x : x.capitalize(), metadata['tags']))))
            #determine original_data
            del metadata['tags']
            metadata["fname"] = fname
            metadata["mids(class_label_id)"] = list(mid_set)
            original_data = metadata

            # generate and save json file
            audio_json = {'text': text, 'tags': tags, 'original_data': original_data}
            json_dump(audio_json, json_save_path)
            file_id += 1

    process("dev")
    process("eval")