# Audiostock Data Card
## Dataset Overview
|Size of dataset|Number of audios|
|:----:|:-----:|
|5.8 GB| 22572|
## Data Collection

|Source|<center>Collecting Method<center>|
|:---------:|:--------|
| [Audiostock Website](https://audiostock.net/se)  |1.Scrape sound effects audio files URLs and the title of effects from Audiostock website. 2. Create meta.csv - file with audio file URLs and titles. 3. Download mp3 audio file for each row in meta.csv and create audio-json pairs for each <br>
## Preprocessing Principles

You may refer to [preprocess_audiostock.py](/data_preprocess/preprocess_audiostock.py) for all the details. Here is a concise summary:

We retrieve information
from the meta data (meta.csv) and form a 3-field `.json` file for each audio. Here are some audio-json pairs selected from the processed dataset:



https://user-images.githubusercontent.com/64437243/200237210-18ce4718-4be4-45a3-86b5-88d02371a3c8.mov



```json
{
    "text": [
        "Bubble 02"
    ],
    "tag": [
        "foam",
        "Bubble sound",
        "dangerous",
        "bubble",
        "air",
        "water",
        "water sound",
        "liquid",
        "rupture",
        "plosive sound",
        "asmr",
        "everyday life sound",
        "noise",
        "image",
        "boiling",
        "science",
        "chemical reaction",
        "experiment",
        "cooking",
        "horror",
        "suspense",
        "painful",
        "Bukku",
        "bukubuku",
        "bokkoshi",
        "bokoboko",
        "poke",
        "pokopoko",
        "Copop",
        "copacopo"
    ],
    "original_data": {
        "title": "Audiostock dataset",
        "Description": "Sound effects scraped from the audiostock.net website",
        "URL": "https://audiostock.net/audio/1150592/play",
        "scene": "",
        "purpose": "Video",
        "impression": "Horror",
        "audio_size": 2.0
    }
}
```




### I. Json file generation principles 
-  **` text  entry`** We take title of the sound effect and put it into test attribute.
-  **` tag  entry`** We use tags from Audiostock website.
-  **` original data`** We save URL, scene, purpose and impression (all those attributes are present on Audiostock website) for every audio as well as audio duration, the dataset name and dataset description.

### II. Audio filtering principles
1. Keep audios with sampling rate higher than **16KHZ** and discard the rest.
2. Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
3. Split evry audio in segements with one sentence in each.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).

