# MACS 
## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
| [MACS Zenodo page](https://zenodo.org/record/5114771#.yq4kbnbmlb1)  |in MACS Zenodo page, download MACS.yaml, find [TAU Urban Acoustic Scenes 2019, Development dataset](https://zenodo.org/record/2589280#.Yxag43bMJhE) and download it. |

## Preprocessing Principles
You may refer to [preprocess_MACS_yuchen.py](/data_preprocess/preprocess_MACS_yuchen.py) for all the details. Here we just offer a concise summary:
### Overview
Some audio-json pairs selected from the processed dataset:

https://user-images.githubusercontent.com/64437243/188529274-9cb2e8ac-fd97-46f6-8690-d7247271f2d2.mov

```json

{
    "text": [
        "ball game with the ball bouncing and people running",
        "some adults are talking",
        "adults talking with an unrecognizable sound in the background"
    ],
    "tag": [
        "adults talking",
        "footsteps"
    ],
    "original_data": {
        "title": "MACS",
        "filename": "airport-stockholm-12-488-a.wav",
        "annotator_ids": [
            354,
            353,
            272
        ]
    }
}
```


https://user-images.githubusercontent.com/64437243/188529311-38f148e8-f518-44a1-911d-2b4773f9f6d2.mov



```json
{
    "text": [
        "motorcycle growling people talking someone coughs",
        "footsteps followed by some alarm and a person coughing while chatting",
        "people are talking traffic noise"
    ],
    "tag": [
        "traffic noise",
        "adults talking",
        "siren",
        "footsteps"
    ],
    "original_data": {
        "title": "MACS",
        "filename": "public_square-helsinki-111-3230-a.wav",
        "annotator_ids": [
            197,
            262,
            366
        ]
    }
}

```
### I. Json file generation principles 
We use information retrieved from MACS.yaml.
-  **` text  entry`**  For each audio, in MACS.yaml, we can find 4-5 sentences offered respectively by different annotators, we collect them and put them here as a list of string. 
- **`tag  entry`** Each annotator also provides a list of tags for each audio, we collect them and put them here as a list of string. (no duplicates)
- **`original_data  entry`** `annotator_ids`(a list of annotators' ids), `filename`(the name of the audio file in TAU2019 dataset) are put here. 
### II. Audio filtering principles
Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
