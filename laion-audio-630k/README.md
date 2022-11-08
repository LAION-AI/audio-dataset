# LAION-Audio-630K Dataset
LAION-Audio-630K is a large-scale audio-text dataset consisting of 633,526 pairs with the total duration of 4,325.39 hours.  It contains audios of human activities, natural sounds and audio effects, consisting of 8 data sources (see the [*data source table*](#data-sources) below) from publicly available websites.  We collect these datasets by downloading audios and relevant text descriptions. Based on our current knowledge, LAION-Audio-630K is the largest audio-text dataset publicly available and a magnitude larger than previous audio-text datasets (by 2022-11-05).

## Content
Among the 8 datasets, we **only release 4 of them (BBC sound effects, Freesound, Epidemic Sound and Audiostock)** under [csv format](#csv-format), since they are public available by anyone through URL links provided by correspondent websites. However, as to the others, i.e. Free To Use Sounds, Sonniss Game Effects, We Sound Effects and Paramount Motion Sound Effects, we would not release them because they are pruchased by LAION. 

### CSV Format
CSV files are of the following structure:
  
  | <sub>url</sub> | <sub>caption1</sub> | <sub>caption2</sub> | <sub>...</sub> | <sub>caption_t5</sub> | <sub>{metadata1}</sub> | <sub>{metadata2}</sub> | <sub>...</sub> | 
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

- **url**: The URL of the audio file
- **caption_i**: the i-th caption of the audio file
- **caption_t5**: For Epidemic Sound, we adopted keywords-to-caption data augmentation using T5 model. Details could be found in the datacard of Epidemic Sound. 
- **{metadata_i}**: Metadata could be the freesound id of the audio etc. 

### Datacards
We provide a datacard for each dataset we processed, which record how we process it. If you want to learn more about caption generation as well as details of **keywords-to-caption data augmentation**, please read datacards available [here](/data_card/) (for Epidemic Sound dataset).    

### About Freesound
We provide two version of Freesound dataset.
- **Freesound (full)**: The original Freesound dataset. Details could be found in its datacard.
- **Freesound (no overlap)**: Made based on Freesound(full), with samples from ESC50, FSD50K, Urbansound8K and Clotho removed. Three related csv files are offered:
  - **csv_train+test**: containing both training and test set of Freesound(no overlap).
  - **csv_train**: training set of Freesound(no overlap).
  - **csv_test**: test set of Freesound(no overlap).
## Data Sources
| Name                                             |Duration                 |Number of Samples   |Data Type                     | Source                                                                                                                                                                                                             | Data Card |                               
|--------------------------------------------------|-------------------------|--------------------|---------                     |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------- |
| Freesound (no overlap)                           |2817.31hrs               | 460801             |1-2 captions per audio, audio    | [website](https://freesound.org/) <br> [csv_train+test](https://drive.google.com/file/d/1sm9pjPBEdXe1qGaGkiPRPj0Dq9cv0DPR/view?usp=sharing)<br>[csv_train](https://drive.google.com/file/d/1xekQ_mR_8-qEyzXmn5G7CGnWHb36XKdH/view?usp=sharing)<br>[csv_test](https://drive.google.com/file/d/1k7CnYjbkFZxNhtiP0vA7zLbM72xuG47G/view?usp=sharing)|[data card](/data_card/freesound.md)|
| Freesound (full)                                 |3033.38hrs               | 515581             |1-2 captions per audio, audio    | [website](https://freesound.org/) <br> [csv](https://drive.google.com/file/d/10LRzpJN7CweCceuI_rXKpUafzilGFAir/view?usp=sharing)                                                |[data card](/data_card/freesound.md)|
| Epidemic Sound                                   |220.41hrs                | 75645              |2 captions per audio, audio    | [website](https://www.epidemicsound.com/sound-effects/) <br> [csv](https://drive.google.com/file/d/1og3gk2V1t52XSPStpJECJ4OzfDMFX3Do/view?usp=sharing)                                |[data card](/data_card/Epidemic_sound.md)           |     
| Audiostock                                       |46.30hrs                 | 10000              |1 caption per audio, audio    | [website](https://audiostock.net/se) <br> [csv](https://drive.google.com/file/d/1FnOcrb6fREIDBzB2lknJnszVn-yNCPp6/view?usp=sharing)                                                           |[data card](/data_card/Audiostock.md) |                
| BBC Sound Effects                                |463.48hrs                | 15973              |1 caption per audio, audio    | [website](https://sound-effects.bbcrewind.co.uk/) <br> [csv*(no longer available, click to see explication below)](#about-bbc-sound-effects)                                                                                                                                |[data card](/data_card/BBC.md)| 
| Free To Use Sounds                               |175.73hrs                | 6370               |Filename as caption, audio    | [website(need purchasing)](https://www.freetousesounds.com/product/all-in-one-sound-library-bundle/)                                                                                          |                                  | 
| Sonniss Game effects                             |84.6hrs                  | 5049               |Filename as caption, audio    | [website(need purchasing)](https://sonniss.com/gameaudiogdc/)                                                                                                                                 |                                  | 
| We Sound Effects                                 |12.00hrs                 | 488                |Filename as caption, audio    | [website(need purchasing)](https://www.wesoundeffects.com/)                                                                                                                                   |                                  | 
| Paramount Motion Sound Effects                   |19.49hrs                 | 4420               |Filename as caption, audio    | [website(need purchasing)](https://www.paramountmotion.com/odeon-sound-effects)                                                                                                               |                                  | 

#### *About BBC Sound Effects
Recently, BBC sound effects have modified their website structure. In consequence, only 300 samples are available for download. So, unfortunately, we are no longer able to generate csv file using our old scripts. In the meantime, many scrappers exist on GitHub, such as https://github.com/alisomay/bbc-sound-effects-downloader. You may try them to see if they work.


## Credits & Licence
- **!!!Term of use!!!**: **By downloading audios through the links provided in the csv files, you agree that you will use the audios for research purposes only, unless you get the permission from owners of the Datasource that you can use it for other purposes.**
- Freesound Credit: This repository uses many sounds from freesound,
for the full list see here: https://drive.google.com/file/d/1kBH5M5zY_7ucHzktw_ng5AgqqV-J-Daq/view?usp=sharing (You may also find extra information about freesound dataset in this file)

## Acknowledgement
The whole collection process as well as all usage of the LAION-Audio-630K are conducted by Germany non-profit pure research organization [LAION](https://laion.ai/). All contributors and collectors of the dataset are considered as open source contributors affiliated to LAION. We would like to appreciate their efforts on this project! 
