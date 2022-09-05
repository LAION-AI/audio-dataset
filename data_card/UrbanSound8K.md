
# UrbanSound8K 
## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
| [UrbanSound8K website](https://urbansounddataset.weebly.com/urbansound8k.html)  |in [UrbanSound8K website](https://urbansounddataset.weebly.com/urbansound8k.html), fill in the download form then the dataset is available directly.|

## Preprocessing Principles
You may refer to [preprocess_UrbanSound8K.py](https://github.com/LAION-AI/audio-dataset/blob/main/data_preprocess/preprocess_UrbanSound8K.py) for all the details. Here we just offer a concise summary:
### Overview
Some audio-json pairs selected from the processed dataset:



https://user-images.githubusercontent.com/64437243/188514643-e725ceb7-af62-4f3f-9206-c3fed9b9d6a2.mov


      
```json
{
    "text": [
        "The sound of siren."
    ],
    "original_data": {
        "freesound_id": 123688,
        "start_time(in original recording)": 14.175572,
        "end_time": 18.175572000000003,
        "salience": "background",
        "class_id": 8,
        "file_name": "123688-8-0-0.wav",
        "fold": 2,
        "author": "lonemonk"
    },
    "tag": [
        "siren",
        "background"
    ]
}
```

      
      


https://user-images.githubusercontent.com/64437243/188514649-091b1cf6-f3a4-4d13-aab6-6db5df35a75b.mov





```json
{
    "text": [
        "The sound of engine idling."
    ],
    "original_data": {
        "freesound_id": 209864,
        "start_time(in original recording)": 1.580937,
        "end_time": 5.5809370000000005,
        "salience": "foreground",
        "class_id": 5,
        "file_name": "209864-5-0-0.wav",
        "fold": 4,
        "author": "davidbain"
    },
    "tag": [
        "engine idling",
        "foreground"
    ]
}
```







### I. Json file generation principles 
 
 Information about  `file_name`, `freesound_id`, `start`, `end`, `salience_id`, `fold` and `class_id` are offered within the two `.csv` metadata files: `UrbanSound8K.csv` and `freesoundsource.csv`.  
-  **` text  entry`**  There are not any human-written captions available, hence we have to make up caption by this template: 
    > "The sound of " + class_label (retrieved according to `class_id`) + "."    
- **`tag  entry`** In UrbanSound8K, each audio has just a unique class label, we put it here.
- **`tag  entry`** All above information in the two `.csv` files mentioned above are stored here
### II. Audio filtering principles
3. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
