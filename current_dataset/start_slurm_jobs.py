import os
import glob

paths = glob.glob('/fsx/knoriy/raw_datasets/mswc/audio/*.tar.gz')

for path in paths:
    os.system( f"srun --comment clap --output=outs/%j.out --exclusive /fsx/home-knoriy/miniconda3/envs/audio_dataset/bin/python /fsx/knoriy/code/audio-dataset/current_dataset/preprocess_mswc.py --job {path} &")