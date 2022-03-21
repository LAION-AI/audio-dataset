import librosa
import glob
from tqdm import tqdm
import os

data_dir = '/mnt/yusong_tianyu/processed_dataset/Clotho'
file_extension = 'flac'
file_list = glob.glob(f'{data_dir}/**/*.{file_extension}', recursive=True)
total_duration = 0
for file in tqdm(file_list):
    total_duration += librosa.get_duration(filename=file)

os.system('date')
print(f'Total {len(file_list)} files, '
      f'total duration of {total_duration / 3600 :.2f} hours.')
