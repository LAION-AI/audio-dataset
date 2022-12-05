import os
import shutil
import argparse
import glob
import random
import numpy as np
from tqdm import tqdm

random.seed(1234)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default=None, help='data directory')
    parser.add_argument('--output_dir', type=str, default=None, help='output directory')
    args = parser.parse_args()

    test_portion = 0.1

    splits = ['train', 'test']

    file_list = glob.glob(f'{args.data_dir}/**/*.flac', recursive=True)
    random.shuffle(file_list)

    split_idx = int(np.round(len(file_list) * test_portion))
    test_list = file_list[:split_idx]
    train_list = file_list[split_idx:]
    split_file_list = {'train': train_list, 'test': test_list}

    file_id = 1
    for split in splits:
        split_output_dir = os.path.join(args.output_dir, split)
        os.makedirs(split_output_dir, exist_ok=True)
        for audio_file in tqdm(split_file_list[split]):
            json_file = audio_file.replace('.flac', '.json')
            audio_save_path = os.path.join(split_output_dir, f'{file_id}.flac')
            audio_json_save_path = audio_save_path.replace('.flac', '.json')
            shutil.move(audio_file, audio_save_path)
            shutil.move(json_file, audio_json_save_path)
            file_id += 1
