# FSD50K 
## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
|[Dataset in Zenodo](https://zenodo.org/record/4060432#.Yv6aInbMJhE) <br>[ontology.json](https://github.com/audioset/ontology/blob/master/ontology.json) | Directly Download|

## Preprocessing Principles
You may refer to [preprocess_FSD50K.py](https://docs.google.com/document/u/0/d/1wDdLZc1zlsVs-hrwsIN9yyZqb-qx9HfOxD_veq3BCbA/edit) for all the details. Here we just offer a concise summary:
### Overview
Some audio-json pairs selected from the processed dataset:



https://user-images.githubusercontent.com/64437243/188525091-4ac692ad-9aef-4c4c-983f-262c6fb7723b.mov


      
```json
{
    "text": [
        "The sounds of Speech, Human voice and Babbling"
    ],
    "original_data": {
        "title": "dadadaduhahhhh.wav",
        "description": "9 month old baby boy making various baby noises, vocalizations, and actual baby behavior performances. More stories about a heroic man who fights against the capitalist hordes everyday to bring home pureed bananas.",
        "license": "http://creativecommons.org/licenses/by/3.0/",
        "uploader": "NoiseCollector",
        "fname": "113237",
        "mids(class_label_id)": ["/m/09x0r","/m/09l8g","/m/0261r1"]
    },
    "tag": [
        "Vocal","Human voice","Foley","Human","Free","Gibberish","Speech","Baby","Recording","Noisecollector","Child","Babbling","Boy"
    ]
}
```

https://user-images.githubusercontent.com/64437243/188525108-b1b6394c-da47-4b4e-be0f-5cdd030dea59.mov



```json
{
    "text": [
        "The sounds of Musical instrument, Wind instrument, woodwind instrument, Flute and Music"
    ],
    "original_data": {
        "title": "Flute - A4 - bad-dynamics",
        "description": "Recorded in the context of the good-sounds.org project from the Music Technology Group, Universitat Pompeu Fabra, Barcelona.\nPart of the Good-sounds dataset of monophonic instrumental sounds.\n\ninstrument::flute\nnote::A\noctave::4\nmidi note::57\nmicrophone::neumann U87\ntuning reference::442\ngood-sounds-id::184\n\n\nIntentionally played as an example of bad-dynamics",
        "license": "http://creativecommons.org/licenses/by/3.0/",
        "uploader": "MTG",
        "fname": "354546",
        "mids(class_label_id)": ["/m/04szw","/m/085jw","/m/0l14j_","/m/04rlf"]
    },
    "tag": [
        "woodwind instrument","Music","Good-sounds","Wind instrument","Single-note","Musical instrument","Flute","Neumann-u87","Multisample","A4"
    ]
}
```



### I. Json file generation principles 
Retrieve all corresponding class labels’ ids from two files:

* FSD50K.ground_truth/{type}.csv
* FSD50K.metadata/collection/collection_{type}.csv

Then read the .json file ontology.json mentioned in the section “Downloading” to get the real class labels associated with ids retrieved. The next step is to determine the contents of .json file:
-  **` text  entry`** Since FSD50K does not contain any human-written captions, we must make up captions using this template: if we have class labels A, B and C, then we let the caption be 
     > "The sounds of A, B and C". 
- **`tag  entry`** All the class labels retrieved are stored here.

- **`original_data entry`** We put here all extra information retrieved from these 4 files: 
    1. dev/eval.csv 
    2. collection_dev/eval.csv 
    3. ontology.json 
    4. dev/eval_clips_info_FSD50K.json
 
### II. Audio filtering principles
 Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
