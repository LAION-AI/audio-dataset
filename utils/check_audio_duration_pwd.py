import librosa
import glob
from tqdm import tqdm
import os

data_dir = ''
file_extension = 'wav'
file_list = glob.glob(f'{data_dir}/**/*.{file_extension}', recursive=True)
total_duration = 0
error_number = 0
for file in tqdm(file_list):
    try:
        total_duration += librosa.get_duration(filename=file)
    except:
        error_number += 1
        print("the error file is:", file)
        continue
os.system('date')
print(f'Total {len(file_list)} files, '
      f'total duration of {total_duration / 3600 :.2f} hours.')
print("error times:", error_number)
