
# List of dataset currently being processed

## Peoples Speech

### Source

`https://mlcommons.org/en/peoples-speech/`

Audio

``` bash
wget https://the-peoples-speech-west-europe.bj.bcebos.com/part-00000-07a8f0d3-6d27-4299-887a-dc12a6d72f8d-c000.tar?authorization=bce-auth-v1/0ef6765c1e494918bc0d4c3ca3e5c6d1/2021-12-03T06%3A30%3A22Z/-1/host/444b9c082ceffd10f38bb965679ed9ec12202836831e111dd193fde281062d26
```

Metadata

``` shell
wget https://the-peoples-speech-west-europe.bj.bcebos.com/part-00000-4e132642-c01c-4db6-9db0-a1e19193f6f8-c000.json?authorization=bce-auth-v1/0ef6765c1e494918bc0d4c3ca3e5c6d1/2021-12-03T06%3A31%3A22Z/-1/host/d7dacf3c31d2e3670d82727636ce234be27a9128df7a80883b84b4a3d8c7f6c0
```

### Processing steps

Utilising Montreal Forced Aligner (MFA), we extract alignments from given source audio and transcript. The alignments produce temporal and phonemes alignments. this is later used to find the optimal area to split the audio into multiple shorter 5 to 10 second segments.

### Dataformat

The raw data consists of `.flac` audio files and `manifest` a json file containing the directory of file an its corresponding transcription.

These original `.flac` are split and a corresponding transcript file is generated for each split audio-text pairs.

### Stats

original: 23.7 Million Audio-Text pairs, Duration: roughly 14.5s each
processed: 47 Million Audio-Text pairs, Duration: roughly 5-10s each