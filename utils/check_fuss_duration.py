import librosa
import glob
from tqdm import tqdm
import os

data_types = ["ssdata","ssdata_reverb"]
for data_type in data_types:
    data_dir = f'./mixture/{data_type}'
    file_extension = 'wav'
    splits = ["train","validation","eval"]
    total_duration = 0
    total_nb = 0
    for split in splits:
        file_list = glob.glob(f'{data_dir}/{split}/*.{file_extension}', recursive=False)
        total_nb += len(file_list)
        for file in tqdm(file_list):
            total_duration += librosa.get_duration(filename=file)

    os.system('date')
    print(f'in {data_type} folder Total {total_nb} files, '
          f'total duration of {total_duration / 3600 :.2f} hours.')