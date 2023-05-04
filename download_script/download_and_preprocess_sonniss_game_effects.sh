#!/bin/bash

conda activate audio_clip

mkdir /mnt/audio_clip/dataset_creation/raw_datasets/sonniss_game_effects
cd /mnt/audio_clip/dataset_creation/raw_datasets/sonniss_game_effects

wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/sonniss_game_effects/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/sonniss_game_effects
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/sonniss_game_effects/*

python data_check/remove_bad_flac.py --dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/sonniss_game_effects/

cd /mnt/audio_clip/audio-dataset/data_preprocess
python split_and_rename.py --data_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/sonniss_game_effects/

cd /mnt/audio_clip/audio-dataset/
python ./utils/make_tar.py \
--input /mnt/audio_clip/dataset_creation/preprocessed_dataset/sonniss_game_effects/ \
--output /mnt/audio_clip/dataset_creation/webdataset_tar/sonniss_game_effects/ \
--dataclass all