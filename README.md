<div align = "center">
<a href="./data_collection/README.md"><img src= "https://img.shields.io/badge/%20-List%20of%20all%20Datasets-red" width = "170px" /></a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://github.com/orgs/LAION-AI/projects/2/views/1"><img src= "https://img.shields.io/badge/%20-Github%20Project%20Page-red" width = "175px" /></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="./data_preprocess/README.md"><img src= "https://img.shields.io/badge/%20-Data%20Process%20Pipeline-red" width = "190px" /></a>
</div> 
<br><br><br>


<div align = "center">
<a href="./laion-audio-630k/README.md"><img src= "https://img.shields.io/badge/-LAION--Audio--630K-red" width = "400px" /></a>
</div> 
<br><br>

# What is Audio Dataset Project?

This repository is created for Audio Dataset Project, an audio dataset collection initiative announced by [LAION](https://laion.ai/). These datasets, each containing enormous amount of audio-text pairs, will be eventually processed and used for training CLAP (Contrastive language-Audio Pretraining) model and other models.

Here is an [explicative video](https://youtu.be/U16VyK2eIYU) introducing you to the project.


# Who are we?

Since Audio Dataset is an open source project belongs to LAION, we have a team of open source contributors. They are, along with LAION members, a three-people researchers group including [Yusong Wu](https://lukewys.github.io/), [Ke Chen](https://www.knutchen.com/) and [Tianyu Zhang](https://mila.quebec/en/person/tianyu-zhang/) from [Mila](https://mila.quebec/) and [UCSD](https://ucsd.edu/), intern [Marianna Nezhurina](https://github.com/marianna13),  previous intern [Yuchen Hui](https://github.com/YuchenHui22314), as well as many enthusiastic contributors from all over the world, such as @PiEquals4#1909 in Discord server.

# What have we done?

- We are keeping collecting audio datasets and here is the [LIST](./data_collection/README.md) of all what we found.
- We define the standard and method to store and process all audio datasets, which is essential in the sense of unifying the final format of datasets to simplify model training. The final dataset format we used for now is [webdataset](https://github.com/webdataset/webdataset). The concrete data process pipeline is specified [here](data_preprocess/README.md) 
- You may also find the processing [code](./data_preprocess/) for each processed audio datasets, respectively. Dependencies required for testing these scripts are specified in the document [`environment.txt`](./data_preprocess/environment.txt). Please Note that [environment.txt](./data_preprocess/environment.txt) may be an non-exhaustive list. There is also a list with redundant packages [environment.yml](./data_preprocess/environment.yml)(i.e. superclass $\supset$ of the exhaustive list), and you can use command `conda env create --name envname --file=environment.yml` to create the environment and `conda activate envname` for using it. 

# Contributing

## Contact

- You could find us on LAION [Discord Server](https://discord.com/invite/eq3cAMZtCC) CLAP channel (the channel name is clap in lower case).
- In the CLAP channel, If you have any question about the project, please feel free to talk with intern **Marianna Nezhurina(marianna13#7139)**, Christoph Schuhmann(@spirit-from-germany#1488), Richard(@rvencu#4120), Romain(@rom1504#5008),Yuchen Hui(@Yuchen Hui#8574), Yusong Wu(@Yusong Wu#3047), Ke Chen(@Ke Chen#0709) or Tianyu Zhang(@tianyuzhang#1725). Text in parenthesis is Discord id.
- Moreover, if you need computation resources during contributing, please go into compute-allocation channel of Discord Server and read the **pinned messages** for usage of LAION pods. If any problem is encountered, please feel free to ask any question in the channel.
- **7.14 update**: old LAION pods are not accessible any more, so you have to ask Richard(@rvencu#4120) in CLAP channel for access to **new LAION cluster**.

## Project progress

We have created a [github project page](https://github.com/orgs/LAION-AI/projects/2) to keep track of the progress of data collection and data processing. Here follows some descriptions for each board of the project:

- **Todo board** : In this board is placed all the datasets in the [LIST](./data_collection/README.md) that is not yet converted to webdataset form and on which nobody is currently working
- **Assigned/In progress/Processing board:** We listed datasets that is assigned to someone for processing, i.e. we have already contributors working on these datasets.
- **Review board:**  Once a certain dataset is converted to webdataset format, the corresponding item should be moved here, indicating that it is ready for further review (e.g. check if there is any format error in order to ensure the quality of model training) by our team.
- **Done board:**  If there is no problem found at the review stage, the dataset will be archived to “Done” board, meaning it is ready for training the model.

## How to contribute?

There are mainly two ways to contribute to our audio dataset project.

1. **Collection of scattered audio sources by means of web scraping technique (and then convert them to webdataset format, i.e. the second point below)**. 
    > Example: crawling word-pronunciation pair from Cambridge Dictionary, or scrape videos from youtube, extract the sound and associate then with the title.
    
    Please join us in Discord if you want to know which scattered audio sources we currently focus on, or if you have suggestion about what we should scrape next.
    
2. **Process of curated datasets, i.e. convert them to webdataset format** according to the [pipeline](./data_preprocess/README.md)
    > Example: [Clotho](https://zenodo.org/record/4783391#.Yr4en3bMLb2) is an curated audio dataset having its own format, thought we ought to convert it to webdataset format with aid of `data_preprocess/preprocess_clotho.py` and `utils/make_tars.py` . For more processing details please read the pipeline part.
    
    For this type of contribution, it is suggested to **view the datasets in the Todo board** in the  [github project page](https://github.com/orgs/LAION-AI/projects/2) and join us in Discord server. **Please contact Marianna Nezhurina(marianna13#7139)** in CLAP channel after you have chosen one **from** **Todo board** to process, so that we can keep track of the progress and avoid the case where many people work simultaneously on one dataset.
    

-  Last but not least, if you find any interesting curated datasets (e.g. Clotho), you can tell us in LAION Discord server. We will eventually add it to the [LIST](data_collection/README.md)

## Contribution Delivery 

Ideally, in both cases mentioned above, we hope **receive from you the webdataset format dataset**. When you’ve packed up your dataset into webdataset format, **upload it** to our AWS S3 bucket: `aws s3 cp your/webdataset/ s3://s-laion-audio/webdataset_tar/your webdataset/` and **contact Marianna Nezhurina(marianna13#7139)** so that she could move the dataset to the review board. (If possible, please also add the processed (not yet packed up) dataset to `S3://s-laion-audio/processed_dataset`). 

When it comes to AWS s3 accessibility problem, please see the LAION cluster part in [contact](#contact) entry above, because AWS s3 are accessible if visited from the LAION new cluster.

Nevertheless, **for the scrapped dataset, we also receive a CSV file** of which the structure is:

`url_link_to_the_audio_allowing_us_to_download     ,      text`          

i.e. each line is an audio_url-text pair, by which we can write a batch file to handle it easily.

# The End
Last updated on July 14 0:57 EST, 2022
Last updated on September 5th 11:00 EST, 2022 (Marianna Nezhurina will take over the intern's work of Yuchen Hui)
Last updated on November 8th 18:55 EST, 2022 (Release of LAION-Audio-630K dataset)
