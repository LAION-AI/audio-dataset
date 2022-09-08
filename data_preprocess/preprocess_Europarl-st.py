"""
Code for preprocess Europarl-ST dataset:
https://www.mllp.upv.es/europarl-st/
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.file_utils import json_load, json_dump
from utils.audio_utils import audio_to_flac
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

def read_lst_file(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
    return lines

if __name__ == '__main__':
    data_dir = '/audio-dataset/Datasets/v1.1'
    output_dir = '/audio-dataset/processed_datasets/Europarl-ST'

    # transfer "train, dev, test, train-noisy" to "train, test, valid".
    split_output_name_dict = {
        'train': 'train',
        'dev': 'valid',
        'test': 'test',
        #'train-noisy': 'train-noisy'       # This split contains many errors
    }

    languages = ['es', 'de', 'en', 'fr', 'nl', 'pl', 'pt', 'ro', 'it']


    dict_skeleton = {'es': None, 'de': None, 'en': 'None', 'fr': None, 'nl': None, 'pl': None, 'pt': None, 'ro': None, 'it': None}

    speech_skeleton = {'es': 'Una persona esta diciendo: ', 'de': 'Eine Person sagt: ',
                        'en': 'A person is saying: ', 'fr': 'Une personne dit: ', 
                        'nl': 'Een persoon zegt: ', 'pl': 'Osoba mówi: ', 
                        'pt': 'Uma pessoa está dizendo: ', 'ro': 'Spune o persoană: ', 
                        'it': 'Una persona sta dicendo: '}

    file_ids = {'train': 1, 'dev': 1, 'test': 1}
    
    for source_lang in languages:

        print(f"Processing {source_lang} dataset...\n")

        language_folder = os.path.join(data_dir, source_lang)

        destination_languages = languages.copy()
        destination_languages.remove(source_lang)
        
        for split in split_output_name_dict.keys():
            
            os.makedirs(os.path.join(output_dir, split_output_name_dict[split]), exist_ok = True)
            segments_dict = {}

            for dest_lang in destination_languages:

                segments_lst_file = os.path.join(language_folder, dest_lang, split, 'segments.lst')
                segments_source_lang_file = os.path.join(language_folder, dest_lang, split, f'segments.{source_lang}')
                segments_dest_lang_file = os.path.join(language_folder, dest_lang, split, f'segments.{dest_lang}')
                
                segments_timestamps = read_lst_file(segments_lst_file)
                segments_source_lang_transcriptions = read_lst_file(segments_source_lang_file)
                segments_dest_lang_transcriptions = read_lst_file(segments_dest_lang_file)

                segments_source_lang_transcriptions_dict = dict(zip(segments_timestamps, segments_source_lang_transcriptions))
                segments_dest_lang_transcriptions_dict = dict(zip(segments_timestamps, segments_dest_lang_transcriptions))
             
                for segment in segments_timestamps:

                    segments_dict.setdefault(segment, dict_skeleton.copy())                                        
                    segments_dict[segment][source_lang] = segments_source_lang_transcriptions_dict[segment]                   
                    segments_dict[segment][dest_lang] = segments_dest_lang_transcriptions_dict[segment]
            
            for segment in segments_dict:
                audio, segment_start, segment_end = segment.split()

                audio_path = os.path.join(language_folder, 'audios', f'{audio}.m4a')
                audio_output_path = os.path.join(output_dir, split_output_name_dict[split], f'{file_ids[split]}.flac')
                json_output_path = os.path.join(output_dir, split_output_name_dict[split], f'{file_ids[split]}.json')

                audio_to_flac(audio_path, audio_output_path, sample_rate = AUDIO_SAVE_SAMPLE_RATE, segment_start = segment_start, segment_end = segment_end)

                audio_json = {
                    "text": [speech_skeleton[source_lang] + f'"{segments_dict[segment][source_lang]}"'],
                    "tag": ['Speech', 'Politician', 'Parliament'],
                    "original data": {  # Metadata
                        "title": "Europarl-ST Dataset",
                        "description": "Europarl-ST is a Multilingual Speech Translation Corpus, that contains paired audio-text samples for Speech Translation, constructed using the debates carried out in the European Parliament in the period between 2008 and 2012.",
                        "transcriptions": segments_dict[segment],
                    }
                }
                
                json_dump(audio_json, json_output_path)
                file_ids[split] += 1