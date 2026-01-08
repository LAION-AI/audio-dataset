# Dataset preprocessing pipeline

Audio Dataset for training CLAP and other models. In this readme, we define the standard and method to store and process
the audio data. Please feel free to propose idea or comments for this documentation. We will iterate several rounds to
have a final version. If something confuses you while reading this doc, you can refer to [the end of this doc](#example-of-the-entire-pipeline) for a complete example. If you are still confused after that, **do please contact us** at discord!!!!!!!

## Overview

For audio dataset, our data process pipline is: <br> Raw dataset -> <br>Processed dataset (audio+json) -> <br> Webdataset (set of`.tar`).

## Raw dataset

The raw dataset refers to the raw form of the dataset as they downloaded (For example, downloaded datasets released on Zenodo). They might have various file format, and might have metadata, captions, or labels, stored in different format. We will take the raw dataset and process them to a unified data storage format.

Please find the list of all datasets we have found [here](../data_collection/README.md) in our github repository.
## Processed dataset

> !! **Important** !!: For the terminology (3 terms: caption, class label and tag) we will use below, **please find their explanation** [here](../data_collection/README.md/#data-type-terminology-explanation). 

The processed dataset contains only audio files and its labels. The audio is saved in `.flac` format with a sample rate
of `48000`. The label of the audio, including captions/class labels/tags/metadata, are stored in a `.json` file with
same filename as the `.flac` file. The file is renamed in processed dataset, and name format in processed dataset is in
number id (`1.wav`, `1.json`), to avoid parsing error in subsequent processing caused by file name.

### Json file format specification and explanation 


The label of the audio is saved in a `.json` file as a dictionary form. The keys of the dictionary and its format are specified as follows:


#### `text`   
 The value of key `text` should be a list of strings where each string is a [caption](../data_collection/README.md/#data-type-terminology-explanation). The example below demonstrates a text with 5 captions in its list:
  ```json
  {
    "text": ["A wooden door creaks open and closed multiple times.", 
    "A creaky door opens and then is shut.", 
    "A vent releases air in the background and a hinge creaks close by.", 
    "An air vent in the background and a hinge creaking in the foreground.", 
    "The squeaky door gets louder the more it moves, Then it suddenly slams shut."]
  }
  ```
  The captions in the list of `text` will be used to form audio-text pair, which is indispensable for the model training. Thus the list must not be empty. Therefore, for those curated datasets who do not offer any caption, **we have to make up a caption from** their [class labels](../data_collection/README.md/#data-type-terminology-explanation).
  - you may refer to the method adopted by us of making up captions for AudioSet and FSD50K: if we have class labels A, B and C, then we let the caption be "The sounds of A, B and C".  

  With regard to Speech datasets with transcript, we prefer to make up the caption like this: `The person is saying "<transcript>"`. If more information are offered by datasets, such as emotions while speaking, please contact Yuchen Hui and discuss with him how to adapt the make-up method so that the caption could include these extra elements.
#### `tag` 
 Note: the entry name is "tag" instead of "tags"!!! The tags of the audio. Its value is a list of strings`i.e. "tag":["str1","str2",...]` where each string could be either a class label (e.g., AudioSet) or a tag (in terms of this [definition](../data_collection/README.md/#data-type-terminology-explanation)). **Note that even if some class labels are utilized for making up captions for the `text` key, they should always be listed here.** See the complete example below for a list containing both class labels used in caption fabrication and several tags.
#### `original_data` 
 Any form of original data associated with the audio. Can be in arbitrary form as long as consistent inside dataset. For example, if the original data of the audio is not in the form of tag or text description, you could save the original data here. In fact, all metadata other than `text` and `tag` should be stored here.

#### `Please add more to here if you come up with more types of label)`

#### An example of .json file selected from processed FSD50K dataset:
```json
{
    "text": ["The sounds of Musical instrument, Harp and Music"],// Made up text description from class labels
    "tag": ["Music", "Oriental", "Game-development", "Intro", "Film-production", "Harp", "Oriental-harp", "Musical instrument", "Bonus-sound"], 
    "original_data": { // metadata
        "title": "Oriental Harp 3", 
        "description": "A professional quality sound effect of an Oriental Harp intro/fill. Suited to game development, film production and media use.", 
        "license": "http://creativecommons.org/licenses/by/3.0/",
        "uploader": "Soughtaftersounds", "fname": "145450", 
        "mids(class_label_id)": ["/m/04szw", "/m/03m5k", "/m/04rlf"]}
}
```
### Preprocess scripts

In `data_preprocess`folder, you could find the codes and scripts for each raw dataset. If you contribute to process a
new dataset, **please add your scripts to `data_preprocess`folder**.

You can find the codes to process audio files in `utils/audio_utils`. You can begin with learning from the codes if you would love to contribute.

An example of preprocess raw dataset can be found at [`data_preprocess/preprocess_clotho.py`](/data_preprocess/preprocess_clotho.py) or [`data_preprocess/preprocess_MACS_yuchen.py`](/data_preprocess/preprocess_MACS_yuchen.py).

### Split the Dataset

For each raw dataset, we should leave-out part of the dataset as test set. When generating `.flac` and `.json` files,
please also split the dataset. The `.flac` and `.json` files should be generated under the folder of the split name.

For datasets that have a split itself (e.g., Clotho or AudioSet), use the dataset split and name it as
train/valid/test (for only two splits, name train/test). For datasets that have custom splits (e.g., AudioSet), name the
split according to the dataset split. If there is no split of the dataset, please randomly leave-out 10% of the dataset
as test set.

Note that we have a tool aiming at doing this, the path is `/data_preprocess/split_and_rename.py`.

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

## Webdataset format 
### Making tar files
To get to Webdataset format, we need the auxiliary function `tardir` in the `make_tar_utils.py` (will be used in file `make_tar.py`). This function creates the `.tar` files that includes the audio and text files in the same folder. One can indicate how much pairs of files should be in the `.tar` file. For example, calling this `make_tar_utils.tardir(file_path='PATH\TO\THE\WHERE\AUDIO_TEXT_PAIRS\LOCATE', tar_name='PATH\TO\THE\OUTPUT\FOLDER\TARFILENAME', n_entry_each=some int number)` will give you `n_entry_each` pairs of (audio, text) files pairs in each tar files naming like `TARFILENAME0`, `TARFILENAME1` etc. All the audio `.flac` and text `.json` files in `file_path` will be packed up.

The `load_from_tar` load `(audio, text, name)` tuples from a specific `.tar` file with some choice of audio decoding
parameters. See the documentation of the function in detail. And, of course, we have a different function for
the `dataloader`. This function is just for debugging and reading `.tar` files temporarily.

### Final step: pack up files to webdataset format
We use the [webdataset](https://github.com/webdataset/webdataset) as the final format to save the data for better
data-loading performance when training the models. The webdataset packs all the files in processed dataset into several
`.tar` files. Each `.tar` files contain a subset of the processed dataset files. These `.tar` files would be the one
read by dataloader when we train the models.

The standard of webdataset and ways to create the webdataset:
```
python make_tar.py --input /mnt/audio_clip/processed_datasets/audiocaps/ --output /mnt/audio_clip/webdataset_tar/audiocaps/ --dataclass all --num_element 512 --filename name
```
- Note that `make_tar.py` makes use of the fonction `tardir` mentioned above.
- It is suggested to use absolute path for --input and --output arguments.

**Meaning of this command**:
- We are expecting (`.flac`, `.json`) file pairs in `/mnt/audio_clip/processed_datasets/audiocaps/{}/` where {} could be `train`, `test`, `valid` which should be indicate in `dataclass`. (See the example at the end of the document)

```
......
   ├── 
   preprocessed_dataset_dir
   ├── audiocaps
   │   ├── train
   │   ├── valid
   │   └── test
```

- We will have outputed tar files like `/mnt/audio_clip/webdataset_tar/audiocaps/train/name0.tar`. Each tar includes 512 (`.flac`, `.json`) file pairs.
- We will have outputed `sizes.json` indicating the size of each `tar` file in the folder.
```
......
   ├── 
   webdataset_tar
   ├── audiocaps
   │   ├── train
   |   |     ├── sizes.json
   |   |     ├── name0.tar
   |   |     ├── name1.tar
   |   |     └── ...
   │   ├── valid
   |   |     ├── sizes.json
   |   |     ├── name0.tar
   |   |     ├── name1.tar
   |   |     └── ...
   │   └── test
             └── ...
```

The outputed `sizes.json` will be like
```
{
    "name0.tar": 512,
    "name1.tar": 512,
    ...
}
```

## Data Check
To make sure that all datasets uploaded to `s3://s-laion-audio` are bug-free and usable, we invite every contributor to follow the three steps of data check below:

1. Before using `FFmpeg` to convert any audio files to `.flac` format, please apply method `soundfile.read()` from python [`soundfile`](https://pysoundfile.readthedocs.io/en/0.8.0/#soundfile.SoundFile) module to every audio file in raw dataset. If any exception is threw when applying soundfile.read() to an audio, then we consider that this audio is broken and we just discard it and will not convert it to `.flac` format (i.e. it will not be included in the final dataset.). You can use [`check_audio.py`](/data_check/check_audio.py) for this. (See the example at the end of this document.)

2. After using `FFmpeg` to convert all audio files into `.flac` format while before they are packed up with json files: repeat the process mentioned in point 1. Discard those flac audios with exception threw when read by `soundfile.read()`.You can use [`check_audio.py`](/data_check/check_audio.py) for this. (See the example at the end of the document.)

3. Once a dataset is converted to Webdataset format and uploaded to `s3://s-laion-judio/webdatset_tar/`, we have to check it for the last time: Using the script written described [here](https://github.com/LAION-AI/CLAP/tree/clap#test-if-tar-is-invalid) to check that the tar files are indeed not broken.

## Data Card
Aiming at archiving the methods we used to processed datasets, we decide to make a "data card" for each dataset. As a result, we invite you to make a data card for datasets you processed. You may refer to [the data card of freesound dataset](/data_card/freesound.md)  as a template.

There are two essential parts in a data card:
1. Data collection: In this part we write how we collect the dataset, which includes two aspects:
   - the source of the dataset, usually an URL
   - the collecting method, could be, for example, downloading directly or scrawling a website, etc.
2. Preprocessing principles:
   - we hope you can put 2 audio-json pairs as an illustration for the preprocessing principles. However, the audio format have to be `.mp4` or `.mov` (so have to be video format, audio format will not work 555) to be supported by github markdown engine. You can refer to this: https://stackoverflow.com/questions/44185716/add-audio-in-github-readme-md
   - **json file generation principle:** (most important part)
      - **What is the content of "text" entry** (most important, since we will use this to train the model)
      - what is the content of "tag" entry 
      - what is the content of "original_data" entry
   - audio filtering principles and audio format specification: same for all datasets, so just copy that of freesound dataset.

## Example of the entire pipeline
We provide an example to illustrate the entire process. The example is based on the MACS dataset.
```bash
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
cd /fsx/yuchen/check_tar/
# data check after uploading
python3 test_tars.py --tar-path "pipe:aws s3 --cli-connect-timeout 0 cp s3://s-laion-audio/webdataset_tar/MACS/train" --start 0 --end 7 --batch-size 1 --order  
python3 test_tars.py --tar-path "pipe:aws s3 --cli-connect-timeout 0 cp s3://s-laion-audio/webdataset_tar/MACS/test" --start 0 --end 1 --batch-size 1 --order  
```
## Contribute

To contribute, please make a branch of yourself and make pull requests to the main branch.

**If you contribute to process a new dataset, please add your process/scraping scripts to `audio-dataset/data_preprocess`folder. If possible, please add the processed (not yet packed up) dataset to `S3://s-laion-audio/webdatset_tar`**

**If you contribute to process a new dataset, please move the final webdataset to the AWS S3 bucket: `S3://s-laion-audio/webdataset_tar/`.**
