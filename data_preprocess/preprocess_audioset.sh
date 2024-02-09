#!/bin/bash

# preliminary: create /tmp/audioset, clone code from audio-dataset

cd /tmp/audioset
mkdir metadata
cd metadata

wget http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/eval_segments.csv
wget http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/balanced_train_segments.csv
wget http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/unbalanced_train_segments.csv
wget https://raw.githubusercontent.com/audioset/ontology/master/ontology.json

cd /fsx/knoriy/code/audio-dataset

for i in $(seq -w 00 40)
do
  aws s3 cp s3://s-laion-audio/raw_dataset/audioset/unbalanced_train_segments/unbalanced_train_segments_part"${i}"_partial.zip /tmp/audioset/zip/
  aws s3 cp s3://s-laion-audio/raw_dataset/audioset/unbalanced_train_segments/unbalanced_train_segments_part"${i}"_partial.z01 /tmp/audioset/zip/
  aws s3 cp s3://s-laion-audio/raw_dataset/audioset/unbalanced_train_segments/unbalanced_train_segments_part"${i}"_partial.z02 /tmp/audioset/zip/

  7z e /mnt/audio_clip/audioset/zip/unbalanced_train_segments_part"${i}"_partial.zip -o/mnt/audio_clip/audioset/audios

  python data_preprocess/preprocess_audioset.py \
  --metadata_dir /tmp/audioset/metadata \
  --metadata_name unbalanced_train_segments \
  --wav_dir /tmp/audioset/audios \
  --output_dir /tmp/audioset/processed_data

  # rm /tmp/audioset/zip/unbalanced_train_segments_part"${i}"_partial*
  # rm -rf /tmp/audioset/audios
done

aws s3 cp s3://s-laion-audio/raw_dataset/audioset/balanced_train_segments.zip /tmp/audioset/
aws s3 cp s3://s-laion-audio/raw_dataset/audioset/eval_segments.zip /tmp/audioset/

cd /tmp/audioset/
unzip balanced_train_segments.zip
unzip eval_segments.zip

cd /fsx/knoriy/code/audio-dataset

python data_preprocess/preprocess_audioset.py \
--metadata_dir /tmp/audioset/metadata \
--metadata_name balanced_train_segments \
--wav_dir /tmp/audioset/balanced_train_segments \
--output_dir /tmp/audioset/processed_data_balanced_train_segments

python data_preprocess/preprocess_audioset.py \
--metadata_dir /tmp/audioset/metadata \
--metadata_name eval_segments \
--wav_dir /tmp/audioset/eval_segments \
--output_dir /tmp/audioset/processed_data_eval_segments

python data_check/remove_bad_flac.py --dir /tmp/audioset/processed_data_eval_segments
python data_check/remove_bad_flac.py --dir /tmp/audioset/processed_data_balanced_train_segments
python data_check/remove_bad_flac.py --dir /tmp/audioset/processed_data

python ./utils/make_tar.py \
--input /tmp/audioset/processed_data \
--output /tmp/audioset/webdataset_tar/unbalanced_train/ \
--dataclass none \
--delete_file

python ./utils/make_tar.py \
--input /tmp/audioset/processed_data_balanced_train_segments \
--output /tmp/audioset/webdataset_tar/balanced_train/ \
--dataclass none \
--delete_file

python ./utils/make_tar.py \
--input /tmp/audioset/processed_data_eval_segments \
--output /tmp/audioset/webdataset_tar/eval/ \
--dataclass none \
--delete_file

aws s3 cp /tmp/audioset/webdataset_tar/balanced_train s3://s-laion-audio/webdataset_tar/audioset_description/balanced_train --recursive
aws s3 cp /tmp/audioset/webdataset_tar/eval s3://s-laion-audio/webdataset_tar/audioset_description/eval --recursive
aws s3 cp /tmp/audioset/webdataset_tar/unbalanced_train s3://s-laion-audio/webdataset_tar/audioset_description/unbalanced_train --recursive