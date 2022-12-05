## Relative Datasets in ICASSP Paper 

| Name                                             |Duration                 |Number of samples   |Disk Space| Source                                                                                 |Data source     |                 
|--------------------------------------------------|-------------------------|--------------------|----------|----------------------------------------------------------------------------------------|----------------|
| AudioSet                                         |5420hrs                  | 1951460            | 758.6GB  | [website](https://research.google.com/audioset/)                                       |Audioset        |
| BBC sound effects                                |463.48hrs                | 15973              | 154.6GB  | [website](https://sound-effects.bbcrewind.co.uk/) <br> [csv]()                         |                |         
| AudioCaps                                        |144.94hrs                | 52904              | 35.5GB   | [website](https://audiocaps.github.io/)                                                |Audioset        |
| Clotho dataset                                   |37.0hrs                  | 5929               | 6.4GB    | [website](https://zenodo.org/record/4783391#.ygdaa9-znpy)                              |Free sound      |
| Free To Use Sounds                               |175.73hrs                | 6370               | 50.7GB   | [website](https://www.freetousesounds.com/product/all-in-one-sound-library-bundle/)    |                |
| Sonniss Game effects                             |84.6hrs                  | 5049               | 22.5GB   | [website(need purchasing)](https://sonniss.com/gameaudiogdc/)                          |                |                                                      
| WeSoundEffects                                   |12.00hrs                 | 488                | 3.3GB    | [website(need purchasing)](https://www.wesoundeffects.com/)                            |                |                                                    
| Paramount Motion - Odeon Cinematic Sound Effects |19.49hrs                 | 4420               | 2.1GB    | [website(need purchasing)](https://www.paramountmotion.com/odeon-sound-effects)        |                |
| UrbanSound8K                                     |8.75hrs                  | 8732               | 1.9GB    | [website](https://urbansounddataset.weebly.com/urbansound8k.html)                      |Free sound      |
| FSD50K                                           |108.3hrs                 | 51197              | 14.6GB   | [website](https://annotator.freesound.org/fsd/release/fsd50k/)                         |Free sound      |
| ESC-50                                           |2.78hrs                  | 2000               | 403.4MB  | [website](https://github.com/karolpiczak/esc-50)                                       |Free sound      |
| Audiostock                                       |46.30hrs                 | 10000              | 5.8GB    | [website](https://audiostock.net/se)                                                   |                |
| MACS - Multi-Annotator Captioned Soundscapes     |10.92hrs                 | 3930               | 2.6G     | [website](https://zenodo.org/record/5114771#.yq4kbnbmlb1)                              |                |
| Freesound                                        |3003.38hrs               | 515581             | 647.0GB  | [website](https://freesound.org/) <br> [csv](https://drive.google.com/file/d/1WroT5fU3o0s-iztotest3yT0XiHqaA0w/view?usp=sharing)|Free sound      |         
| Freesound (audio from other datasets excluded)   |2817.31hrs               | 460801             | 611.0GB  | [website](https://freesound.org/) <br> [csv (same as )](https://drive.google.com/file/d/1WroT5fU3o0s-iztotest3yT0XiHqaA0w/view?usp=sharing)|Free sound      |         
| VGG Sound                                        |501.27hrs                | 180879             | 72.9GB   | [website](https://www.robots.ox.ac.uk/~vgg/data/vggsound/)                             |                |    
| wavtext5k                                        |25.48hrs                 | 4525               | 5.1GB    | [website](https://github.com/microsoft/WavText5K)                                      |                |
| Epidemic Sound (Sound effect part)               |220.41hrs                | 75645              | 61GB     | [website](https://www.epidemicsound.com/sound-effects/)                                |                |


|Total duration|Total Samples|Total Disk Space|
|--------------|-------------|----------------|
| 10,254.86hrs |2,895,082 pairs|  1,845.003 GB   |

## ICASSP Training Datasets (Some samples from test/validation split are excluded)

<!-- copy the table above, but without the "Disk Space column, add a column called "Data Type"-->
| Name                                             |Duration                 |Number of samples   |Data Type| Source                                                                                 |Data source     |
|--------------------------------------------------|-------------------------|--------------------|---------|----------------------------------------------------------------------------------------|----------------|
| ***AudioSet(unbalanced train)                                         |5311.2hrs                | 1912024            |2 captions per audio,audio    | [website](https://research.google.com/audioset/)                                       |Audioset        |
| BBC sound effects                                |463.48hrs                | 15973              |1 caption per audio, audio    | [website](https://sound-effects.bbcrewind.co.uk/) <br> [csv]()                         |                |
| ***AudioCaps                                        |136.87hrs                | 49274              |1 caption per audio, audio   | [website](https://audiocaps.github.io/)                                                |Audioset        |
| ****Clotho                                    |23.99hrs                 | 3839               |5 captions per audio, audio    | [website](https://zenodo.org/record/4783391#.ygdaa9-znpy)                              |Free sound      |
| Free To Use Sounds                               |175.73hrs                | 6370               |Filename as caption, audio    | [website](https://www.freetousesounds.com/product/all-in-one-sound-library-bundle/)    |                |
| Sonniss Game effects                             |84.6hrs                  | 5049               |Filename as caption, audio    | [website(need purchasing)](https://sonniss.com/gameaudiogdc/)                          |                |
| We Sound Effects                                   |12.00hrs                 | 488                |Filename as caption, audio    | [website(need purchasing)](https://www.wesoundeffects.com/)                            |                |
| Paramount Motion Sound Effects                |19.49hrs                 | 4420               |Filename as caption, audio    | [website(need purchasing)](https://www.paramountmotion.com/odeon-sound-effects)        |                |
| ***FSD50K                                           |70.39hrs                 | 36796              |1 caption per audio, audio    | [website](https://annotator.freesound.org/fsd/release/fsd50k/)                         |Free sound      |
| Audiostock                                       |46.30hrs                 | 10000              |1 caption per audio, audio    | [website](https://audiostock.net/se)                                                   |                |
| ***MACS - Multi-Annotator Captioned Soundscapes     |9.825hrs                 | 3537               |Several (2~) captions per audio, audio    | [website](https://zenodo.org/record/5114771#.yq4kbnbmlb1)                              |                |
| ***Freesound (audio from other datasets excluded)   |2528.15hrs               | 414127             |1-2 captions per audio, audio    | [website](https://freesound.org/) <br> [csv (same as )](https://drive.google.com/file/d/1WroT5fU3o0s-iztotest3yT0XiHqaA0w/view?usp=sharing)|Free sound      |
| ***wavtext5k                                        |23.2hrs                 | 4072               |1 caption per audio, audio    | [website](https://github.com/microsoft/WavText5K)                                      |                |
| Epidemic Sound (Sound effect part)               |220.41hrs                | 75645              |2 captions per audio, audio    | [website](https://www.epidemicsound.com/sound-effects/)                                |                |


<!-- 
esc50_in_fsd50k_train:  399
esc50_in_fsd50k_validation:  60
esc50_in_fsd50k_test:  171
esc50_in_clotho_train:  94
esc50_in_clotho_validation:  27
esc50_in_clotho_test:  34
usd8k_in_fsd50k_train:  697
usd8k_in_fsd50k_validation:  180
usd8k_in_fsd50k_test:  341
usd8k_in_clotho_train:  411
usd8k_in_clotho_validation:  150
usd8k_in_clotho_test:  209
clotho_test_in_fsd50k_train:  54
clotho_test_in_fsd50k_validation:  15
clotho_test_in_fsd50k_test:  33
fsd50k_test_in_clotho_train:  137
fsd50k_test_in_clotho_validation:  31
fsd50k_test_in_clotho_test:  33
clotho_val_in_fsd50k_train:  53
clotho_val_in_fsd50k_validation:  10
clotho_val_in_fsd50k_test:  31
fsd50k_val_in_clotho_train:  38
fsd50k_val_in_clotho_validation:  10
audiocaps_test_in_audioset_unbalanced_train:  4875
audiocaps_test_in_audioset_balanced_train:  0

-->
## Potential Data Leakage
| Datasource A | Datasource B | Number of Overlap Samples |
|:--------------:|:--------------:|:---------------------------:|
|   ESC50-all  | Clotho-train |             94            |
|   ESC50-all  | Clotho-valid |             27            |
|   ESC50-all  | Clotho-test  |             34            |
|              |              |                           |
|   ESC50-all  | FSD50K-train |            399            |
|   ESC50-all  | FSD50K-valid |             60            |
|   ESC50-all  | FSD50K-test  |            171            |
|              |              |                           |
|   USD8K-all  | Clotho-train |            411            |
|   USD8K-all  | Clotho-valid |            150            |
|   USD8K-all  | Clotho-test  |            209            |
|              |              |                           |
|   USD8K-all  | FSD50K-train |            697            |
|   USD8K-all  | FSD50K-valid |            180            |
|   USD8K-all  | FSD50K-test  |            341            |
|              |              |                           |
| Clotho-test  | FSD50K-train |             54            |
| Clotho-test  | FSD50K-valid |             15            |
| Clotho-test  | FSD50K-test  |             33            |
|              |              |                           |
| FSD50K-test  | Clotho-train |            137            |
| FSD50K-test  | Clotho-valid |             31            |
| FSD50K-test  | Clotho-test  |             33            |
|              |              |                           |
| Clotho-valid | FSD50K-train |             53            |
| Clotho-valid | FSD50K-valid |             10            |
|              |              |                           |
| FSD50K-valid | Clotho-train |             38            |
| FSD50K-valid | Clotho-valid |             10            |
|              |              |                           |
| Audiocaps-test    | Audioset-unbalanced-train     |           4875            |
| Audiocaps-test    | Audioset-balanced-train       |           0            |
|              |              |                           |
|audioset-test  | audiocaps-train |  0 |
|audioset-test  | audiocaps-valid |  0 |