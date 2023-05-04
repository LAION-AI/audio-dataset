#!/bin/bash

cd /mnt/audio_clip

mkdir raw_datasets
cd raw_datasets

wget -r -np -nH --cut-dirs=1 -R index.html # URL
wget -r -np -nH --cut-dirs=1 -R index.html # URL
wget -r -np -nH --cut-dirs=1 -R index.html # URL

cd /mnt/audio_clip/audio-dataset
conda activate audio_clip
python ./data_preprocess/preprocess_audiocaps.py
python ./data_preprocess/preprocess_bbc.py
python ./data_preprocess/preprocess_clotho.py

python ./utils/make_tar.py --input /mnt/audio_clip/processed_datasets/audiocaps/ --output /mnt/audio_clip/webdataset_tar/audiocaps/ --dataclass all
python ./utils/make_tar.py --input /mnt/audio_clip/processed_datasets/BBCSoundEffects/ --output /mnt/audio_clip/webdataset_tar/BBCSoundEffects/ --dataclass all
python ./utils/make_tar.py --input /mnt/audio_clip/processed_datasets/Clotho/ --output /mnt/audio_clip/webdataset_tar/Clotho/ --dataclass all
