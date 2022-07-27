# In HPC cluster by stability.ai use
#     singularity pull docker://picapicaxi/audio_dataset_preprocessing:latest
#     singularity shell audio_dataset_preprocessing.sif
# By default, singularity bind mounts /home/$USER, /temp and /$PWD into your 
# container.
FROM ubuntu
# install packages
RUN apt-get update && \
    apt-get install -y vim && \
    apt-get -y install python3 python3-dev python3-pip && \ 
    apt-get -y install ffmpeg && \
    apt-get -y install unrar && \
    pip3 install pandas && \
    pip3 install tqdm && \
    pip3 install librosa  && \
    pip3 install torch && \
    pip3 install webdataset 
    
CMD ["bash"]


