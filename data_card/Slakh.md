# Slakh Data Card

## Dataset Overview
|Size of dataset|Number of audios|Duration|
|:----:|:-----:|:-----:|
|81 GB|18276|1 374 hrs|

## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
| [Slakh2100 Zenodo page](https://zenodo.org/record/4599666#.Y3KGu-zMKWB)  |in Slakh Zenodo page, download `slakh2100_flac_redux.tar.gz`. You can find the original website [here](http://www.slakh.com/) |

## Preprocessing Principles
You may refer to [preprocess_slakh.py](/data_preprocess/preprocess_slakh.py) for all the details. Here we just offer a concise summary:

### Overview
Some audio-json pairs selected from the processed dataset below:


```json
{
    "text": "playing piano music synthesized with scarbee clavinet full plugin",
    "tag": [
        "piano",
        "electric piano 1"
    ],
    "original_data": {
        "audio_rendered": true,
        "inst_class": "Piano",
        "integrated_loudness": -21.746239958311875,
        "is_drum": false,
        "midi_program_name": "Electric Piano 1",
        "midi_saved": true,
        "plugin_name": "scarbee_clavinet_full.nkm",
        "program_num": 4,
        "filename": "Track01595/stems/S04.flac"
    }
}
```
### I. Json file generation principles 
-  **` text  entry`** If a `mix`file was used, text used was `playing mix of {instrument_name1} {instrument_name2} ...` and `stems` use `playing {instrument_name} music synthesized with {plugin_name} plugin`.
-  **` tag  entry`** We use instrument name and MIDI program name as tags.
-  **` original data`** We save filename, instrument class, MIDI program name, plugin name for every audio as well as audio duration, the dataset name and dataset description.
### II. Audio filtering principles
Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
