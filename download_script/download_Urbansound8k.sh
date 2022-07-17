#!/bin/bash
#cd home/yuchen/raw_datasets/UrbanSound8K

mkdir UrbanSound8K
cd UrbanSound8K || exit
wget -c https://zenodo.org/record/1203745/files/UrbanSound8K.tar.gz
cd .. || exit