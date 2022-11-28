# Freesound Data Card
## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
| [Freesound website](https://freesound.org/)  |1.Scrape from the [Freesound website](https://freesound.org/) and get the [metadata](https://github.com/LAION-AI/audio-dataset/blob/main/metadata/freesound/parquet/freesound_parquet.parquetb/main/metadata/freesound/parquet/freesound_parquet.parquet) <br>2. Download according to URLs provided in the metadata file, using a python downloading script|

## Preprocessing Principles

You may refer to [freesonud_preprocess.py](/data_preprocess/preprocess_freesound.py) for all the details. Here is a concise summary:

For each audio, there are 6 fields in the metadata file, respectively named `id`, `title`, `tags`, `description`, `username,` and `download_url`. We retrieve information
from these 6 fields and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:


#### 

https://user-images.githubusercontent.com/64437243/188022285-68272a97-641c-42dc-b408-59afefb96e9a.mov
      
```json
{
    "text": [
    "DSI Tetra - Sample and Hold Me - B4 (Sample & Hold Me-71-127.", 
    "Single note sampled from an analog synthesizer by Modular Samples."
        ],

    "tag": [
    "multisample", "single-note", "synthesizer", "DSI-Tetra", "midi-note-71", "B4"
    ], 
    "original_data": {
        "tags": ["multisample", "single-note", "synthesizer", "DSI-Tetra", "midi-note-71", "B4"], 
        "description": "Single note sampled from an analog synthesizer by Modular Samples.<br>Modular Samples provides samples of vintage and modern synthesizers for Apple EXS24, Native Instruments Kontakt, Reason and Live samplers, with over 50 gigabytes of public domain content.<br>Sampler files and sound packs are also available at <a href =\"http://modularsamples.com\" target=\"_blank\">http://modularsamples.com</a>.<br><br>Synthesizer: DSI Tetra<br>Patch name (pack): Sample and Hold Me<br>Note: B4<br>Midi note: 71<br>", 
        "username": "modularsamples", 
        "download_url": "https://freesound.org/apiv2/sounds/282776/download/", 
        "title": "DSI Tetra - Sample and Hold Me - B4 (Sample & Hold Me-71-127.wav)", 
        "id": 282776
            }
        }
```

<audio id="audio" controls="controls" preload="yes">
      <source id=".flac" src="./2.flac">
</audio>
      
      

https://user-images.githubusercontent.com/64437243/188022499-ee6b5c4b-9e19-4b04-9dfe-c21b821e554c.mov



```json
{
    "text": [
        "futuresoundfx-795.", "Sci-Fi Futuristic Sound Effects From Stolting Media Group."
        ], 
    "tag": [
        "Home-Videos", "DVD", "pod-Cast", "Sound-Effects", "alien-sound-effects", "Remixing", "space", "TV", "media", "Screen", "Video", "Music-Production", "fx", "Recording", "stolting-media-group", "Broadcasting", "effects", "Futuristic", "Alien", "Future", "Radio", "Film"
        ], 
    "original_data": {
        "tags": ["Home-Videos", "DVD", "pod-Cast", "Sound-Effects", "alien-sound-effects", "Remixing", "space", "TV", "media", "Screen", "Video", "Music-Production", "fx", "Recording", "stolting-media-group", "Broadcasting", "effects", "Futuristic", "Alien", "Future", "Radio", "Film"], 
        "description": "Sci-Fi Futuristic Sound Effects From Stolting Media Group. These samples available from <a href=\"http://freesound.org\" rel=\"nofollow\">freesound.org</a> are in mp3 format and for non commercial use only with credit to <a href=\"http://StoltingMediaGroup.com\" rel=\"nofollow\">StoltingMediaGroup.com</a> For a commercial license and high quality WAV format visit <a href=\"http://www.stoltingmediagroup.com\" rel=\"nofollow\">http://www.stoltingmediagroup.com</a>", 
        "username": "stoltingmediagroup", "download_url": "https://freesound.org/apiv2/sounds/158824/download/", 
        "title": "futuresoundfx-795.mp3", 
        "id": 158824
        }
    }
```







### I. Json file generation principles 
-  **` text  entry`**  Both `title` and `description` may contain candidates to fill in the list of `text` entry, therefore we have two possible sources of caption:
    1. Take the content of `title`, remove the potential file extension part of it and replace all the underlines between words with spaces. Let it be the first caption of the audio.
    2. Take the first sentence of the content of `description`. If this sentence contains HTML tags, then discard it. Otherwise, we will let it be the second caption for the audio

    As a result, the text entry eventually looks like  `"text": [processed title, first sentence of description without HTML tags]`. When training we will randomly choose one of them in the list to be the caption.

- **`tag  entry`** Just take `tags:` field of the metadata file split by delimiter `,` as the content of `tag` entry.
- **`original_data  entry`** All the six fields’ contents are stored here.
### II. Audio filtering principles
1. Keep samples no longer than **3** minutes, and discard the rest.
2. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
3. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
