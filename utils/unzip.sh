#!/bin/bash

# unzip.sh - Unzip TAU-urban-acoustic-scenes-2019-development.audio.{1-21}.zip

for i in {1..21}
do
    unzip TAU-urban-acoustic-scenes-2019-development.audio.$i.zip
done