import os
import pandas as pd
import argparse
import glob
from tqdm import tqdm
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.audio_utils import audio_to_flac
from utils.file_utils import json_dump
from utils.dataset_parameters import AUDIO_SAVE_SAMPLE_RATE

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from functools import partial

executor = ProcessPoolExecutor(max_workers=cpu_count())


def get_json(file_path, class_metadata, class_to_name_map):
    audio_id = os.path.basename(file_path).replace('.wav', '')[1:]
    class_labels = class_metadata[audio_id].replace('"', '').split(',')
    class_names = [class_to_name_map[c] for c in class_labels]
    text = "The sounds of " + ", ".join(class_names[:-1]) + " and " + class_names[-1]
    json_data = {'text': text,
                 'original_data': {'class_labels': class_labels,
                                   'class_names': class_names, }
                 }
    return json_data


def process_single_audio(file_path, json_data, output_dir):
    audio_id = os.path.basename(file_path).replace('.wav', '')[1:]  # remove the "Y" in the first character
    json_dump(json_data, output_dir + '/' + audio_id + '.json')
    audio_to_flac(file_path, output_dir + '/' + audio_id + '.flac', sample_rate=AUDIO_SAVE_SAMPLE_RATE)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--metadata_dir', type=str, default=None, metavar='N',
                        help='metadata_dir')
    parser.add_argument('--metadata_name', type=str, default='unbalanced_train_segments', metavar='N',
                        help='metadata_name')
    parser.add_argument('--wav_dir', type=str, default=None, metavar='N',
                        help='wav_dir')
    parser.add_argument('--output_dir', type=str, default=None, metavar='N',
                        help='output_dir')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # Load metadata
    unbalanced_csv_path = os.path.join(args.metadata_dir, f'{args.metadata_name}.csv')
    with open(unbalanced_csv_path, 'r') as f:
        lines = f.readlines()

    lines = lines[3:]
    header_list = ['YTID', 'start_seconds', 'end_seconds', 'positive_labels']
    class_metadata = [l.strip().split(', ') for l in lines]
    class_metadata = pd.DataFrame(class_metadata, columns=header_list)

    class_to_name_map = pd.read_csv(os.path.join(args.metadata_dir, 'class_labels_indices.csv'))

    class_metadata = dict(zip(class_metadata.YTID, class_metadata.positive_labels))
    class_to_name_map = dict(zip(class_to_name_map.mid, class_to_name_map.display_name))

    wav_all = glob.glob(f'{args.wav_dir}/*.wav')
    futures = []
    for file in tqdm(wav_all):
        # process_single_audio(file, class_metadata, class_to_name_map, args.output_dir)
        json_data = get_json(file, class_metadata, class_to_name_map)
        futures.append(
            executor.submit(partial(process_single_audio, file, json_data, args.output_dir)))

    result = [future.result() for future in tqdm(futures)]
