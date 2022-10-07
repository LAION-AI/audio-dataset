'''
Code for preprocess MACS dataset.
use condition: download MACS.ymal from https://zenodo.org/record/5114771#.yq4kbnbmlb1 and put it in the same folder as the script. 
author:
Yuchen Hui 

'''
from p_tqdm import p_map 
import os
import yaml
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

audio_dir = f'/fsx/MACS/TAU2019/TAU-urban-acoustic-scenes-2019-development/audio'
meta_dir = f'/fsx/MACS/TAU2019/MACS.yaml'
output_dir = f'/fsx/yuchen/macs/processed'

def yaml_load(yaml_path):
    with open(yaml_path, 'r') as f:
        dic = yaml.safe_load(f)
        f.close()
    return dic

# this dic contains only one keyvalue pair  
# the value is a list of dic, where each dic corresponds to one audio clip 
# the structure of the dic is:
# {
#     filename:
#     annotations: [{annotaor_id:int, sentence:str, tags:[str]}]
# }
def get_filename(dic):
    return dic["filename"]

def get_all_annotator_ids(dic):
    return [annotation["annotator_id"] for annotation in dic["annotations"]]

def get_all_sentences(dic):
    return [annotation["sentence"] for annotation in dic["annotations"]]

def get_all_tags(dic):
    tags = set()
    for annotation in dic["annotations"]:
        for tag in annotation["tags"]:
            tag = re.sub(r"_+", " ", tag) 
            tags.add(tag)
    return list(tags) 


def process(audio_dic):
    #json
    text = get_all_sentences(audio_dic)
    tag = get_all_tags(audio_dic)
    filename = get_filename(audio_dic)
    original_data = {}
    original_data["title"] = "MACS"
    original_data["filename"] = filename
    original_data["annotator_ids"] = get_all_annotator_ids(audio_dic) 

    json_dic = {"text" : text, "tag" : tag, "original_data" : original_data}

    # determine input/output path
    audio_path = os.path.join(audio_dir, filename)
    flac_file_name = filename.replace(".wav", ".flac")
    audio_save_path = os.path.join(output_dir,flac_file_name)
    json_save_path = audio_save_path.replace('.flac', '.json')

    # convert audio to flac
    audio_to_flac(audio_path, audio_save_path, AUDIO_SAVE_SAMPLE_RATE) 

    # save json
    json_dump(json_dic, json_save_path)

if __name__ == '__main__':

    dic = yaml_load(meta_dir)
    file_list = dic["files"]
    # in the list, each element is a dict, of which the structure is:
    # {
    #     filename:
    #     annotations: [{annotaor_id:int, sentence:str, tags:[str]}]
    # }
    p_map(process, file_list, num_cpus=32)



