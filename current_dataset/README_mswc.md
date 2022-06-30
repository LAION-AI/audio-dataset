# List of dataset currently being processed

## Multilingual Spoken Words Corpus

### Source

`https://mlcommons.org/en/multilingual-spoken-words/`

Audio and Metadata

``` bash
wget https://storage.googleapis.com/public-datasets-mswc/mswc.tar.gz
```

### Processing steps

MSWC consists of two layers of compression. We  first decompress the first layer, at each  language we decompress and convert `.opus` to `.flac`. Simultaneously we generate the json dump by traversing and cleaning the provided `.csv`.

### Dataformat

Origin

``` shell
mswc
│
└─── lang1
│   └─── audio
│       └─── clips
│           └─── .opus
│       └─── splits
│           └─── .csv
│   └───alignments
└─── lang2
│    └─── audio
│       └─── clips
│           └─── .opus
│       └─── splits
│           └───.csv
|   |   ...
```

processed

``` shell
mswc
│
└─── lang1
│   └─── train
│       │    .json
│       └─── .opus
│   └─── test
│       │    .json
│       └─── .opus
│   └─── valid
│       │    .json
│       └─── .opus
└─── lang2
│   └─── train
│       │    .json
│       └─── .opus
│   └─── test
│       │    .json
│       └─── .opus
│   └─── valid
│       │    .json
│       └─── .opus
|   |   ...
```

### Stats

- 50  languages

original: 23.7 Million Audio-Text pairs, Duration: roughly 1s each
processed: 47 Million Audio-Text pairs, Duration: roughly 1s each