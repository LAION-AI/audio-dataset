# MACS 
## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
| [Slakh2100 Zenodo page](https://zenodo.org/record/4599666#.Y3KGu-zMKWB)  |in Slakh Zenodo page, download `slakh2100_flac_redux.tar.gz`. You can find the original website [here](http://www.slakh.com/) |

## Preprocessing Principles
You may refer to [preprocess_slakh.py](/data_preprocess/preprocess_slakh.py) for all the details. Here we just offer a concise summary:

### Overview
Some audio-json pairs selected from the processed dataset:

### II. Audio filtering principles
Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
