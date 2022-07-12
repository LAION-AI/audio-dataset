# audio-dataset

Audio Dataset for training CLAP and other models. In this readme, we define the standard and method to store and process
the audio data. Please feel free to propose idea or comments for this documentation. We will iterate several rounds to
have a final version.

## Overview

For audio dataset, our data process pipline is: <br> Raw dataset -> <br>Processed dataset (audio+json) -> <br> Webdataset (set of`.tar`).

## Raw dataset

The raw dataset refers to the raw form of the dataset as they downloaded (presumably from [https://deploy.laion.ai](https://deploy.laion.ai)). They might have various file format, and might have metadata, captions, or labels, stored in different format. We will take the raw dataset and process them to a unified data storage format.

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
#### `tag` 
 The tags of the audio. Its value is a list of strings where each string could be either a class label (e.g., AudioSet) or a tag (in terms of this [definition](../data_collection/README.md/#data-type-terminology-explanation)). **Note that even if some class labels are utilized for making up captions for the `text` key, they should always be listed here.** See the complete example below for a list containing both class labels used in caption fabrication and several tags.
#### `original_data` 
 Any form of original data associated with the audio. Can be in arbitrary form as long as consistent inside dataset. For example, if the original data of the audio is not in the form of tag or text description, you could save the original data here. In fact, all metadata other than `text` and `tag` should be stored here.

#### `Please add more to here if you come up with more types of label)`

#### An example of .json file selected from processed FSD50K dataset:
```json
{
    "text": ["The sounds of Musical instrument, Harp and Music"],// Made up text description from class labels
    "tags": ["Music", "Oriental", "Game-development", "Intro", "Film-production", "Harp", "Oriental-harp", "Musical instrument", "Bonus-sound"], 
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

## Webdataset format 
### Making tar files
To get to Webdataset format, we need the auxiliary fonction `tardir` in the `make_tar_utils.py` (will be used in file `make_tar.py`). This function creates the `.tar` files that includes the audio and text files in the same folder. One can indicate how much pairs of files should be in the `.tar` file. For example, calling this `make_tar_utils.tardir(file_path='PATH\TO\THE\WHERE\AUDIO_TEXT_PAIRS\LOCATE', tar_name='PATH\TO\THE\OUTPUT\FOLDER\TARFILENAME', n_entry_each=some int number)` will give you `n_entry_each` pairs of (audio, text) files pairs in each tar files naming like `TARFILENAME0`, `TARFILENAME1` etc. All the audio `.flac` and text `.json` files in `file_path` will be packed up.

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

**Meaning of this command**:
- We are expecting (`.flac`, `.json`) file pairs in `/mnt/audio_clip/processed_datasets/audiocaps/{}/` where {} could be `train`, `test`, `valid` which should be indicate in `dataclass`.

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

## Directory Structure

Raw dataset: All the raw datasets are stored in [https://deploy.laion.ai](https://deploy.laion.ai). For contributors, you can also freely download datasets by visiting links offered in the [list](../data_collection/README.md). For those datasets who do not have any link in the list, they are purchased by LAION hence we can not make it public due to license issue. Do please contact us if you want to process them.

Preprocessed dataset & webdataset: all the preprocessed dataset & webdataset are stored in AWS S3 bucket: `S3://s-laion-audio/webdataset_tar/` 
If you contribute to process a new dataset, please move the final webdataset to the above location.

## Contribute

To contribute, please make a branch of yourself and make pull requests to the main branch.

If you contribute to process a new dataset, please add your scripts to `data_preprocess`folder.

If you contribute to process a new dataset, please move the final webdataset to the AWS S3 bucket. 
