#!/bin/bash

cd /mnt/audio_clip

mkdir raw_datasets
cd raw_datasets

wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaaa/Clotho/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/audiocaps/
wget -r -np -nH --cut-dirs=1 -R index.html https://deploy.laion.ai/0fed69941baaabaeccedc2aaaaaaaaab/BBCSoundEffectsComplete/

cd /mnt/audio_clip/audio-dataset
conda activate audio_clip
python ./data_preprocess/preprocess_audiocaps.py
python ./data_preprocess/preprocess_bbc.py
python ./data_preprocess/preprocess_clotho.py