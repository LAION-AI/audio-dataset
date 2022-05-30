#!/bin/bash

conda activate audio_clip

mkdir /mnt/audio_clip/dataset_creation/raw_datasets/paramount_motion
cd /mnt/audio_clip/dataset_creation/raw_datasets/paramount_motion

wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaaa/Paramount%20Motion%20-%20Odeon%20Cinematic%20Sound%20Effects%20Pack/

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/paramount_motion/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/paramount_motion
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/paramount_motion/*

python data_check/remove_bad_flac.py --dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/paramount_motion/

cd /mnt/audio_clip/audio-dataset/data_preprocess
python split_and_rename.py --data_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/paramount_motion/

cd /mnt/audio_clip/audio-dataset/
python ./utils/make_tar.py \
--input /mnt/audio_clip/dataset_creation/preprocessed_dataset/paramount_motion/ \
--output /mnt/audio_clip/dataset_creation/webdataset_tar/paramount_motion/ \
--dataclass all \
--delete_file
