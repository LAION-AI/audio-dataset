#!/bin/bash
# /fsx/MACS/TAU2019/TAU-urban-acoustic-scenes-2019-development/audio    raw dataset path
# /fsx/yuchen/macs/processed/                                           processed dataset path

cd /fsx/yuchen/macs/
#upload raw dataset to s3
aws s3 cp --recursive /fsx/MACS/TAU2019/TAU-urban-acoustic-scenes-2019-development/audio/ s3://s-laion-audio/raw_dataset/MACS/
# data check before processing:
python3 check_audio.py --dir /fsx/MACS/TAU2019/TAU-urban-acoustic-scenes-2019-development/audio --ext wav  
# data preprocess:
python3 preprocess_MACS_yuchen.py
# data check after processing
python3 check_audio.py --dir /fsx/yuchen/macs/processed --ext flac
# split (train 90% test 10%)
python3 split_and_rename.py --data_dir /fsx/yuchen/macs/processed/  --output_dir /fsx/yuchen/macs/split/   
cd /fsx/yuchen/utils/
# make tar (train)
python3 make_tar.py --input /fsx/yuchen/macs/split --output /fsx/yuchen/macs/webdataset/ --dataclass train --num_element 512     
# make tar (test)
python3 make_tar.py --input /fsx/yuchen/macs/split --output /fsx/yuchen/macs/webdataset/ --dataclass test --num_element 512     
# upload to s3
aws s3 cp --recursive /fsx/yuchen/macs/webdataset/ s3://s-laion-audio/webdataset_tar/MACS/                                      
# data check after uploading
python3 test_tars.py --tar-path "pipe:aws s3 --cli-connect-timeout 0 cp s3://s-laion-audio/webdataset_tar/MACS/train" --start 0 --end 7 --batch-size 1 --order --log-file /fsx/yuchen/checktar/MACS/MACS_train.log &
python3 test_tars.py --tar-path "pipe:aws s3 --cli-connect-timeout 0 cp s3://s-laion-audio/webdataset_tar/MACS/test" --start 0 --end 1 --batch-size 1 --order --log-file /fsx/yuchen/checktar/MACS/MACS_test.log &