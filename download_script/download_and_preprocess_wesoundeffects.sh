#!/bin/bash

conda activate audio_clip

mkdir /mnt/audio_clip/dataset_creation/raw_datasets/wesoundeffects
cd /mnt/audio_clip/dataset_creation/raw_datasets/wesoundeffects

wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaaa/WeSoundEffects/

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/wesoundeffects/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/wesoundeffects
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/wesoundeffects/*

cd /mnt/audio_clip/audio-dataset/data_preprocess
python split_and_rename.py --data_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/wesoundeffects/

cd /mnt/audio_clip/audio-dataset/
python ./utils/make_tar.py \
--input /mnt/audio_clip/dataset_creation/preprocessed_dataset/wesoundeffects/ \
--output /mnt/audio_clip/dataset_creation/webdataset_tar/wesoundeffects/ \
--dataclass all \
--delete_file