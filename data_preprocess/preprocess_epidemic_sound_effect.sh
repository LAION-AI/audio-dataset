#!/bin/bash
# /mnt/epidemic_sound_effects/raw                                       raw dataset path
#  /mnt/epidemic_sound_effects/processed                                processed dataset path

 
#upload raw dataset to s3
aws s3 cp --recursive  /mnt/epidemic_sound_effects/raw s3://s-laion-audio/raw_dataset/epidemic_sound_effects/ || exit
# data check before processing:
cd /home/ubuntu/audio-dataset/audio_check/ || exit 
python3 check_audio.py --dir /mnt/epidemic_sound_effects/raw --ext mp3  || exit
# data preprocess:
cd /home/ubuntu/ || exit
python3 preprocess_Epidemic.py|| exit
# data check after processing
cd /home/ubuntu/audio-dataset/audio_check/ || exit 
python3 check_audio.py --dir /mnt/epidemic_sound_effects/processed --ext flac|| exit
# split (train 90% test 10%)
python3 split_and_rename.py --data_dir /mnt/freesound/processed/  --output_dir /mnt/freesound/split   || exit
cd //yuchen/utils/ || exit
# make tar (train)
python3 make_tar.py --input /mnt/freesound/split --output /mnt/freesound/webdataset/ --dataclass train --num_element 512     || exit
# make tar (test)
python3 make_tar.py --input /mnt/epidemic_sound_/split --output /mnt/freesound/webdataset/ --dataclass test --num_element 512     || exit
# upload to s3
aws s3 cp --recursive /mnt/epidemic_sound_effects/webdataset s3://s-laion-audio/webdataset_tar/epidemic_sound_effects/                                      || exit
# data check after uploading
python3 test_tars.py --tar-path "pipe:aws s3 --cli-connect-timeout 0 cp s3://s-laion-audio/webdataset_tar/epidemic_sound_effects/train" --start 0 --end 7 --batch-size 1 --order --log-file epidemic_sound_effects_train_log.log &
python3 test_tars.py --tar-path "pipe:aws s3 --cli-connect-timeout 0 cp s3://s-laion-audio/webdataset_tar/epidemic_sound_effects/test" --start 0 --end 1 --batch-size 1 --order --log-file epidemic_sound_effects_test_log.log.log &