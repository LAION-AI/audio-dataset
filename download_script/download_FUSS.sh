#!/bin/bash
#cd home/yuchen/raw_datasets/FUSS

mkdir source_pure
cd source_pure || exit
wget -c https://zenodo.org/record/3694384/files/FUSS_fsd_data.tar.gz
wget -c https://zenodo.org/record/3694384/files/FUSS_rir_data.tar.gz
cd .. || exit
mkdir mixture
cd mixture || exit
wget -c https://zenodo.org/record/3694384/files/FUSS_ssdata.tar.gz
wget -c https://zenodo.org/record/3694384/files/FUSS_ssdata_reverb.tar.gz
cd .. || exit