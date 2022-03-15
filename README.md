# audio-dataset

Audio Dataset for training CLAP and other models. In this readme, we define the standard and method to store and process
the audio data. Please feel free to propose idea or comments for this documentation. We will iterate several rounds to
have a final version.

## Overview

For audio dataset, our data process pipline is: raw dataset -> processed dataset (audio+json) -> webdataset (set of
`.tar`).

## Raw dataset

The raw dataset refers to the raw form of the dataset as they downloaded (presumably
from [https://deploy.laion.ai](https://deploy.laion.ai)). They might have various file format, and might have metadata,
captions, or labels, stored in different format. We will take the raw dataset and process them to a unified data storage
format.

## Processed dataset

The processed dataset contains only audio files and its labels. The audio is saved in `.flac` format with a sample rate
of `48000`. The label of the audio, including captions/class labels/tags/metadata, are stored in a `.json` file with
same filename as the `.flac` file.

### Key of each type of label and its format

The key of the data labels and its format:

- captions: The captions or natural text description of the audio. The text is a list containing strings where each
  entry is one caption/description.
- (more TBD): (TODO @yusong)
  (Please add more to here if you come up with more types of label)

### Preprocess scripts

In `data_preprocess`folder, you could find the codes and scripts for each raw dataset. If you contribute to process a
new dataset, please add your scripts to `data_preprocess`folder.

You can find the codes to process audio files in `utils/audio_utils`.

An example of preprocess raw dataset can be found in `data_preprocess/preprocess_clotho.py`.

### Split the Dataset

For each raw dataset, we should leave-out part of the dataset as test set. When generating `.flac` and `.json` files,
please also split the dataset. The `.flac` and `.json` files should be generated under the folder of the split name.

For datasets that have a split itself (e.g., Clotho or AudioSet), use the dataset split and name it as
train/valid/test (for only two splits, name train/test). For datasets that have custom splits (e.g., AudioSet), name the
split according to the dataset split. If there is no split of the dataset, please randomly leave-out 10% of the dataset
as test set.

```
preprocessed_dataset_dir
├── Dataset_A
│   ├── train
│   └── test
├── Dataset_B (if have train/test/split)
│   ├── train
│   ├── valid
│   └── test
└── Dataset_C (if have custom split)
│   ├── train
│   ├── custom_split_1
│   └── custom_split_2
```

## Webdataset

We use the [webdataset](https://github.com/webdataset/webdataset) as the final format to save the data for better
data-loading performance when training the models. The webdataset packs all the files in processed dataset into several
`.tar` files. Each `.tar` files contain a subset of the processed dataset files. These `.tar` files would be the one
read by dataloader when we train the models.

The standard of webdataset and ways to create the webdataset: (TODO @tianyu)

## Directory Structure

Raw dataset: All the raw datasets are stored in [https://deploy.laion.ai](https://deploy.laion.ai).

Preprocessed dataset & webdataset: all the preprocessed dataset & webdataset are stored in (TBD) (TODO: figure out a
place to save). If you contribute to process a new dataset, please move the final webdataset to the above location.