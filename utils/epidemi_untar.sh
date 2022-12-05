#!/bin/bash

cd /mnt/epidemic_sound_effects/epidemic_with_augmentation/train || exit
# untar all .tar file to /mnt/epidemic_sound_effects/epidemic_with_augmentation/split/train
for i in *.tar;
do
tar -xaf $i -C /mnt/epidemic_sound_effects/epidemic_with_augmentation/split/train || exit
echo "train $i is untarred" || exit
done

cd /mnt/epidemic_sound_effects/epidemic_with_augmentation/test || exit
# untar all .tar file to /mnt/epidemic_sound_effects/epidemic_with_augmentation/split/test
for i in *.tar;
do
tar -xaf $i -C /mnt/epidemic_sound_effects/epidemic_with_augmentation/split/test || exit
echo "test $i is untarred" || exit
done
