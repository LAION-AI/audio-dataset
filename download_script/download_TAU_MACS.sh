#!/bin/bash

for i in {1..21}
do
    AUDIO_URL="https://zenodo.org/record/2589280/files/TAU-urban-acoustic-scenes-2019-development.audio.${i}.zip"
    wget -c $AUDIO_URL
done

wget -c https://zenodo.org/record/5114771/files/MACS.yaml

unzip '*.zip'