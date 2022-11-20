from p_tqdm import p_map 
import os
from pathlib import Path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.file_utils import json_load, json_dump
import yaml
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE
from p_tqdm import p_map 
import uuid
from functools import partial


input_dir = Path('/fsx/home-krishna/slakh/slakh2100_flac_redux')
output_dir = Path('/fsx/home-krishna/slakh/processed')

def yaml_load(yaml_path):
    with open(yaml_path, 'r') as f:
        dic = yaml.safe_load(f)
        f.close()
    return dic

def get_stem_text(meta_data, stem_name):
    inst_name = meta_data["stems"][stem_name]["inst_class"].lower()
    plugin_name = meta_data["stems"][stem_name]["plugin_name"].lower().split(".")[0].replace("_", " ")
    text = f"playing {inst_name} music synthesized with {plugin_name} plugin" 
    return text

def get_stem_tags(meta_data, stem_name):
    inst_name = meta_data["stems"][stem_name]["inst_class"].lower()
    midi_program_name = meta_data["stems"][stem_name]["midi_program_name"].lower()
    return [inst_name, midi_program_name]

def get_mix_text(meta_data):
    inst_names = [meta_data["stems"][i]["inst_class"].lower()
                    for i in meta_data["stems"]]

    set_inst_names = ", ".join(set(inst_names))
    text = f"playing mix of {set_inst_names} music" 
    return text

def get_mix_tags(meta_data):
    inst_names = [meta_data["stems"][i]["inst_class"].lower()
                    for i in meta_data["stems"]]
    midi_program_name = [meta_data["stems"][i]["midi_program_name"].lower()
                    for i in meta_data["stems"]]

    return list(set(inst_names)) + list((set(midi_program_name)))

def process_stem(stem_dir, working_dir):
    stem_path = (stem_dir / "stems").iterdir()
    current_output_dir = output_dir / working_dir
    meta_data = yaml_load(stem_dir/ "metadata.yaml")
    
    for current_stem in stem_path:
        stem_name = current_stem.stem
        stem_text = get_stem_text(meta_data, stem_name)
        stem_tags = get_stem_tags(meta_data, stem_name)
        original_data = meta_data["stems"][stem_name]
        original_data["filename"] = str(current_stem.relative_to(current_stem.parent.parent.parent))
        current_uuid = str(uuid.uuid4())

        # Save JSON
        json_dic = {"text": stem_text, "tag": stem_tags, "original_data": original_data}
        json_save_path = current_output_dir  / (current_uuid + ".json")
        json_dump(json_dic, json_save_path)

        # Save FLAC File
        flac_save_path = current_output_dir  / (current_uuid + ".flac")
        audio_to_flac(current_stem, flac_save_path, AUDIO_SAVE_SAMPLE_RATE)

def process_mix(stem_dir, working_dir):
    current_output_dir = output_dir / working_dir
    meta_data = yaml_load(stem_dir/"metadata.yaml")
    meta_data["filename"] = str(stem_dir.relative_to(stem_dir.parent.parent))
    text = get_mix_text(meta_data)
    tag = get_mix_tags(meta_data)
    current_uuid = str(uuid.uuid4())

    # Save JSON
    json_dic = {"text" : text, "tag" : tag, "original_data" : meta_data}
    json_save_path = current_output_dir / (current_uuid + ".json")
    json_dump(json_dic, json_save_path)

    # Save FLAC File
    current_mix = stem_dir /  "mix.flac"
    flac_save_path = current_output_dir  / (current_uuid + ".flac")
    audio_to_flac(current_mix, flac_save_path, AUDIO_SAVE_SAMPLE_RATE)


if __name__ == '__main__':
    splits = ['train', 'validation', 'test']
    for current_dir in splits:
        work_path = input_dir / current_dir
        stem_list = list(work_path.iterdir())

        # Process Stems
        # process_stem(stem_list[0], current_dir)
        p_map(partial(process_stem, working_dir=current_dir), stem_list, num_cpus=24)

        # Process Mix
        #process_mix(stem_list[0], current_dir)
        p_map(partial(process_mix, working_dir=current_dir), stem_list, num_cpus=24)
