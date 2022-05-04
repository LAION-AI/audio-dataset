import glob
import soundfile
import argparse
import os
from tqdm import tqdm

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from functools import partial

executor = ProcessPoolExecutor(max_workers=cpu_count())


def remove_bad_flac(file_path):
    try:
        wav = soundfile.read(file_path)
    except:
        print(file_path)
        os.remove(file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove bad FLAC files.')
    parser.add_argument('--dir', type=str, default='data/flac',
                        help='dir to the FLAC files.')
    args = parser.parse_args()
    data_dir = args.dir
    wav_files = glob.glob(data_dir + '/**/*.flac', recursive=True)
    futures = []
    for wav_file in tqdm(wav_files):
        futures.append(executor.submit(remove_bad_flac, wav_file))
    result = [future.result() for future in tqdm(futures)]
