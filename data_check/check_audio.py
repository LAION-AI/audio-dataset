
import glob
import soundfile
import argparse
import os
from p_tqdm import p_map 

# examples:
# python3 check_audio.py --dir /fsx/MACS/TAU2019/TAU-urban-acoustic-scenes-2019-development/audio --ext wav 
# python3 check_audio.py --dir /fsx/MACS/TAU2019/TAU-urban-acoustic-scenes-2019-development/audio --ext wav --remove
# python3 check_audio.py --dir /fsx/yuchen/macs/processed --ext flac

def audio_check(file_path):
    try:
        wav = soundfile.read(file_path)
        return "good" 
    except:
        with open("audio_check_error.txt", "a") as f:
            print(file_path)
            f.write(file_path + "\n")
        return file_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check (and will remove if you add --remove flag) bad audio files.')
    parser.add_argument(
        '--dir', 
        type=str, 
        default='./', 
        help='dir to the wav files.'
        )
    parser.add_argument(
        '--ext', 
        type=str, 
        default='wav', 
        help='extension of the audio files. to be checked')
    parser.add_argument(
        '--remove', 
        default=False,
        action='store_true',
        help='if add this flag, will remove the bad files')
    args = parser.parse_args()
    data_dir = args.dir
    extension = args.ext
    remove = args.remove

    wav_files = glob.glob(data_dir + f'/**/*.{extension}', recursive=True)
    p_map(audio_check, wav_files, num_cpus=os.cpu_count())

    if remove:
        for wav_file in wav_files:
            if wav_file != "good":
                os.remove(wav_file)
