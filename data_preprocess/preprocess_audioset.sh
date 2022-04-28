#!/bin/bash

# preliminary: create /mnt/audio_clip/audioset, clone code from audio-dataset

cd /mnt/audio_clip/audioset
mkdir metadata
cd metadata

wget http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/eval_segments.csv
wget http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/balanced_train_segments.csv
wget http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/unbalanced_train_segments.csv
wget https://raw.githubusercontent.com/qiuqiangkong/audioset_tagging_cnn/master/metadata/class_labels_indices.csv

cd ~/audio-dataset

for i in $(seq -w 00 40)
do
  aws s3 --region us-east-1 cp s3://laion-audio/raw_dataset/audioset/unbalanced_train_segments/unbalanced_train_segments_part"${i}"_partial.zip /mnt/audio_clip/audioset/zip/
  aws s3 --region us-east-1 cp s3://laion-audio/raw_dataset/audioset/unbalanced_train_segments/unbalanced_train_segments_part"${i}"_partial.z01 /mnt/audio_clip/audioset/zip/
  aws s3 --region us-east-1 cp s3://laion-audio/raw_dataset/audioset/unbalanced_train_segments/unbalanced_train_segments_part"${i}"_partial.z02 /mnt/audio_clip/audioset/zip/

  7z e /mnt/audio_clip/audioset/zip/unbalanced_train_segments_part"${i}"_partial.zip -o/mnt/audio_clip/audioset/audios

  python data_preprocess/preprocess_audioset.py \
  --metadata_dir /mnt/audio_clip/audioset/metadata \
  --metadata_name unbalanced_train_segments \
  --wav_dir /mnt/audio_clip/audioset/audios \
  --output_dir /mnt/audio_clip/audioset/processed_data

  rm /mnt/audio_clip/audioset/zip/unbalanced_train_segments_part"${i}"_partial*
  rm -rf /mnt/audio_clip/audioset/audios
done

aws s3 --region us-east-1 cp s3://laion-audio/raw_dataset/audioset/balanced_train_segments.zip /mnt/audio_clip/audioset/
aws s3 --region us-east-1 cp s3://laion-audio/raw_dataset/audioset/eval_segments.zip /mnt/audio_clip/audioset/

cd /mnt/audio_clip/audioset/
unzip balanced_train_segments.zip
unzip eval_segments.zip

cd ~/audio-dataset

python data_preprocess/preprocess_audioset.py \
--metadata_dir /mnt/audio_clip/audioset/metadata \
--metadata_name balanced_train_segments \
--wav_dir /mnt/audio_clip/audioset/balanced_train_segments \
--output_dir /mnt/audio_clip/audioset/processed_data_balanced_train_segments

python data_preprocess/preprocess_audioset.py \
--metadata_dir /mnt/audio_clip/audioset/metadata \
--metadata_name eval_segments \
--wav_dir /mnt/audio_clip/audioset/eval_segments \
--output_dir /mnt/audio_clip/audioset/processed_data_eval_segments

python ./utils/make_tar.py \
--input /mnt/audio_clip/audioset/processed_data \
--output /mnt/audio_clip/audioset/webdataset_tar/unbalanced_train/ \
--dataclass none \
--delete_file

python ./utils/make_tar.py \
--input /mnt/audio_clip/audioset/processed_data_balanced_train_segments \
--output /mnt/audio_clip/audioset/webdataset_tar/balanced_train/ \
--dataclass none \
--delete_file

python ./utils/make_tar.py \
--input /mnt/audio_clip/audioset/processed_data_eval_segments \
--output /mnt/audio_clip/audioset/webdataset_tar/eval/ \
--dataclass none \
--delete_file

aws s3 --region us-east-1 cp /mnt/audio_clip/audioset/webdataset_tar/balanced_train s3://laion-audio/webdataset_tar/audioset/balanced_train --recursive
aws s3 --region us-east-1 cp /mnt/audio_clip/audioset/webdataset_tar/eval s3://laion-audio/webdataset_tar/audioset/eval --recursive
aws s3 --region us-east-1 cp /mnt/audio_clip/audioset/webdataset_tar/unbalanced_train s3://laion-audio/webdataset_tar/audioset/unbalanced_train --recursive