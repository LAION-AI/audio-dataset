#!/bin/bash
cd /mnt/freesound/old_freesound/train || exit
# untar all .tar file to path mnt/freesound/oldfreesound/split/train 
for i in *.tar;  
do  
tar -xaf $i -C /mnt/freesound/old_freesound/split/train  || exit
echo "train $i is untarred" || exit
done 
cd /mnt/freesound/old_freesound/test || exit
# untar all .tar file to path mnt/freesound/oldfreesound/split/test || exit
for i in *.tar; 
do 
tar -xaf $i -C /mnt/freesound/old_freesound/split/test || exit
echo "test $i is untarred" || exit
done 




