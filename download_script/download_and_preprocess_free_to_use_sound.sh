#!/bin/bash

conda activate audio_clip

mkdir /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds
cd /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds

wget -r -np -nH --cut-dirs=1 -R index.html # URL
wget -r -np -nH --cut-dirs=1 -R index.html # URL

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/*
cd /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds

wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 
wget -r -np -nH --cut-dirs=1 -R index.html # URL 

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/*
cd /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds

wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL
wget -r -np -nH --cut-dirs=1 -R index.html #URL

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/*

python data_check/remove_bad_flac.py --dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds/

cd /mnt/audio_clip/audio-dataset/data_preprocess
python split_and_rename.py --data_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds/

cd /mnt/audio_clip/audio-dataset/
python ./utils/make_tar.py \
--input /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds/ \
--output /mnt/audio_clip/dataset_creation/webdataset_tar/free_to_use_sounds/ \
--dataclass all

