# MACS 
## Data Collection

|Source|Collecting Method|
|:---------:|:--------|
| [Slakh2100 Zenodo page](https://zenodo.org/record/4599666#.Y3KGu-zMKWB)  |in Slakh Zenodo page, download `slakh2100_flac_redux.tar.gz`. You can find the original website [here](http://www.slakh.com/) |

## Preprocessing Principles
You may refer to [preprocess_slakh.py](/data_preprocess/preprocess_slakh.py) for all the details. Here we just offer a concise summary:

### Overview
Some audio-json pairs selected from the processed dataset below or [here](https://github.com/krishnakalyan3/slakh-datacard):

https://github.com/krishnakalyan3/slakh-datacard/raw/main/23.flac

```json
{
   "text":"playing bass music synthesized with scarbee jay bass both plugin",
   "tag":[
      "bass",
      "fretless bass"
   ],
   "original_data":{
      "audio_rendered":true,
      "inst_class":"Bass",
      "integrated_loudness":-25.66588529276208,
      "is_drum":false,
      "midi_program_name":"Fretless Bass",
      "midi_saved":true,
      "plugin_name":"scarbee_jay_bass_both.nkm",
      "program_num":35,
      "filename":"Track01908/stems/S01.flac"
   }
}
```

https://github.com/krishnakalyan3/slakh-datacard/raw/main/24.flac

```json
{
   "text":"playing mix of guitar, strings (continued), synth pad, drums, brass, piano, chromatic percussion, reed, pipe, bass music",
   "tag":[
      "guitar",
      "strings (continued)",
      "synth pad",
      "drums",
      "brass",
      "piano",
      "chromatic percussion",
      "reed",
      "pipe",
      "bass",
      "french horn",
      "electric piano 1",
      "string ensemble 1",
      "tenor sax",
      "acoustic guitar (nylon)",
      "trumpet",
      "drums",
      "electric guitar (jazz)",
      "whistle",
      "vibraphone",
      "electric bass (pick)",
      "baritone sax",
      "pad 2 (warm)"
   ],
   "original_data":{...}
}
```
### I. Json file generation principles 
The json was generated from `metadata.yaml` file within each audio stem. If a `mix`file was used, text used was `playing mix of {instrument_name1} {instrument_name2} ...` and `stems` use `playing {instrument_name} music synthesized with {plugin_name} plugin`
### II. Audio filtering principles
Discard all audios failed to be read by `soundfile.read()` method or denied by FFmpeg while processing.
### III. Audio format specifications
After the preprocessing work, all audio files should be in FLAC format with sampling rate of 48KHZ. (Processed by ffmpeg).
