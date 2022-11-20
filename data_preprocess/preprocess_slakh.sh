#!/bin/bash

# Prepare directories
cd /fsx/home-krishna/slakh/processed
mkdir -p train validation test

# /fsx/home-krishna/slakh/slakh2100_flac_redux                                                                                    # raw dataset path
# /fsx/home-krishna/slakh/processed/                                                                                              # processed dataset path

python3 /fsx/home-krishna/slakh/audio-dataset/download_script/download_slakh.sh                                                   # download RAW data
python3 /fsx/home-krishna/slakh/audio-dataset/data_check/check_audio.py --dir slakh2100_flac_redux/train/ --ext flac              # data check train
python3 /fsx/home-krishna/slakh/audio-dataset/data_check/check_audio.py --dir slakh2100_flac_redux/validation/ --ext flac         # data check validation
python3 /fsx/home-krishna/slakh/audio-dataset/data_check/check_audio.py --dir slakh2100_flac_redux/test/ --ext flac               # data check test
aws s3 cp --recursive /fsx/home-krishna/slakh/slakh2100_flac_redux s3://s-laion-audio/raw_dataset/slakh/                          # Upload RAW to S3

# Preprocess Slakh
python3 /fsx/home-krishna/slakh/audio-dataset/data_preprocess/preprocess_slakh.py                                                 # data preprocess

# Rename the dataset sequentially
python /fsx/home-krishna/slakh/merge_dirs.py --root_dir /fsx/home-krishna/slakh/processed/train --to_rename True
python /fsx/home-krishna/slakh/merge_dirs.py --root_dir /fsx/home-krishna/slakh/processed/test --to_rename True
python /fsx/home-krishna/slakh/merge_dirs.py --root_dir /fsx/home-krishna/slakh/processed/validation --to_rename True
aws s3 cp --recursive /fsx/home-krishna/slakh/processed s3://s-laion-audio/processed_dataset/slakh

# Webdataset
# rename the validation folder (/fsx/home-krishna/slakh/processed) to valid
python3 /fsx/home-krishna/slakh/audio-dataset/utils/make_tar.py --input /fsx/home-krishna/slakh/processed/ --output /fsx/home-krishna/slakh/webdataset --dataclass all --num_element 512
aws s3 cp --recursive /fsx/home-krishna/slakh/webdataset/ s3://s-laion-audio/webdataset_tar/slakh/                                      
