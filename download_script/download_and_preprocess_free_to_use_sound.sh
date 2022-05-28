#!/bin/bash

conda activate audio_clip

mkdir /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds
cd /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds

wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/All%20Sounds%20Edited%20By%20Soundly/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/All%20Sounds%20Edited%20By%20Zapsplat/

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sound
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/*
cd /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds

wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20Of%20Brazil/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20Of%20Cambodia/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20Of%20Canada/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20Of%20Costa%20Rica/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20Of%20Dubai/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20Of%20Greece/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Croatia/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Cyprus/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20France/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Georgia/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Germany/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Hong%20Kong/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Iceland/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Indonesia/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Japan/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Malaysia/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Malta/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Portugal/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Qatar/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Singapore/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20USA/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/Sounds%20of%20Vietnam/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/VR%20Sound%20Library/

cd /mnt/audio_clip/audio-dataset/data_preprocess
python preprocess_filename_dataset.py --data_dir /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/ --output_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sound
rm -r /mnt/audio_clip/dataset_creation/raw_datasets/free_to_use_sounds/*

cd /mnt/audio_clip/audio-dataset/data_preprocess
python split_and_rename.py --data_dir /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds/

cd /mnt/audio_clip/audio-dataset/
python ./utils/make_tar.py \
--input /mnt/audio_clip/dataset_creation/preprocessed_dataset/free_to_use_sounds/ \
--output /mnt/audio_clip/dataset_creation/webdataset_tar/free_to_use_sounds/ \
--dataclass all \
--delete_file

