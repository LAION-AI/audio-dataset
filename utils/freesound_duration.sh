#!/bin/bash

cd /home/yuchen/processed/bbc


#907 101
for ((i=$2; i<=$3 ; i++))
do	 
 	aws s3 cp s3://s-laion-audio/webdataset_tar/freesound/$1/$i.tar /home/yuchen/processed/bbc/$i.tar || exit
	tar -xaf $i.tar || exit
	python3 check_audio_duration.py >> ../trace.txt || exit
	rm -r ./mnt || exit
	rm $i.tar || exit
		
done
cd ../
python3 extract_hrs.py