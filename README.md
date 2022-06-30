# What is Audio Dataset Project?

This repository is created for Audio Dataset Project, an audio dataset collection initiative announced by [LAION](https://laion.ai/). These datasets, each containing enormous amout of audio-text pairs, will be eventually processed and used for training CLAP (Contrastive language-Audio Pretraining) model and other models.

Here is an [explicative video](https://youtu.be/U16VyK2eIYU) introducing you to the project.

# Who are we?

Our team includes LAION members and a researchers group from [Mila](https://mila.quebec/) and [UCSD](https://ucsd.edu/), as well as many enthusiastic contributors from all over the world.

# What have we done?

- We are keeping collecting audio datasets and here is the [LIST](./data_collection/README.md) of all waht we found.
- We define the standard and method to store and process all audio datasets, which is essential in the sense of unifying the final format of datasets to simplify model training. The final dataset format we used for now is [webdataset](https://github.com/webdataset/webdataset). The concret data process pipeline is specified [here](data_preprocess/README.md) 
- You may also find the processing [code](./data_preprocess/) for each processed audio datasets, respectively. Dependencies required for testing these scripts are specified in the document [`environment.txt`](environment.txt). Notice that [environment.txt](data_preprocess/environment.txt) may be an inexhaustive list. 

# Contributing

## Contact

- You could find us on LAION Discord server CLAP channel (the channel name is clap in lower case).
- In the CLAP channel, If you have any question about the project, please feel free to talk with Yuchen Hui, Christoph, Richard V, rom1504, Yusong Wu, Ke Chen or Tianyu Zhang.

## Project progress

We have created a [github project page](https://github.com/orgs/LAION-AI/projects/2) to keep track of the progress of data collection and data processing. Here follows some descriptions for each board of the project:

- **Todo board** : In this board is placed all the datasets in the [LIST](./data_collection/README.md) that is not yet converted to webdataset form and on which nobody is currently working
- **Assigned/In progress/Processing board:** We listed datasets that is assigned to someone for processing, i.e. we have already contributors working on these datasets.
- **Review board:**  Once a certain dataset is converted to webdataset format, the corresponding item should be moved here, indicating that it is ready for further review (e.g. check if there is any format error in order to ensure the quality of model training) by our team.
- **Done board:**  If there is no problem found at the review stage, the dataset will be archived to “Done” board, meaning it is ready for training the model.

## How to contribute?

There are mainly two ways to contribute to our audio dataset project.

1. **Collection of scattered audio sources by means of web scraping technique (and then convert them to webdatset format, i.e. the second point below)**. 
    - Examples: crawling word-pronunciation pair from Cambridge Dictionary, or scrape vedios from youtube, extract the sound and associate then with the titile.
    
    Please join us in Discord if you want to know which scattered audio sources we currently focus on, or if you have suggestion about what we should scrape next.
    
2. **Process of curated datasets, i.e. convert them to webdataset format** according to the [pipeline](./data_preprocess/README.md)
    - Example: [Clotho](https://zenodo.org/record/4783391#.Yr4en3bMLb2) is an curated audio dataset having its own format, thought we ought to convert it to webdataset format with aid of `data_preprocess/preprocess_clotho.py` and `utils/make_tar_utils.py` . For processing details please read the pipeline part.
    
    For this type of contribution, it is suggested to **view the datasets in the Todo board** in the  [github project page](https://github.com/orgs/LAION-AI/projects/2) and join us in Discord server. Please contact Yuchen Hui in CLAP channel after you have chosen one **from** **Todo board** to process, so that we can keep track of the progress and avoid the case where many people work simultaneously on one dataset.
    

-  Last but not least, if you found any interesting curated datasets (e.g. Clotho), you can tell us in LAION Discord server. We will eventually add it to the [LIST](data_collection/README.md)

## Contribution Delivery 

Idealy, in both cases mentionned above, we hope **receive from you the webdataset format dataset**. When you’ve packed up your dataset into webdataset format, **upload it** to our AWS S3 bucket: `aws s3 cp your/webdataset/ s3://s-laion-audio/webdataset_tar/your webdataset/` and **contact Yuchen Hui** so that he could move the dataset to the review board.

Nervertheless, **for the scrapped dataset, we also receive a CSV file** of which the structure is:

`url_link_to_the_audio_allowing_us_to_download     ,      text`          

i.e. each line is an audio_url-text pair, by which we can write a batch file to handle it easily.

# The End