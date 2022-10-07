"""
This module contains auxiliary functions allowing us to download youtube videos
and transform then to .flac with sampling rate of 4800.

This file can also be viewed as a downloading script, 
it accetps the arguments as follows:

    1. --csv_path: path to the csv file. e.g. --csv_path "./data/youtube.csv"
    The csv file format specification is:

        id,start_time,end_time,...
        4kJVb8tPZmw,0,10,...
        ...

        or:

        id,...,...
        4kJVb8tPZmw,...,...
        ....

        !!! Attention: start_time and end_time are in seconds.

    Afterall, the csv file must contain a column named "id", 
    and can optionally contain a column named "start_time" and "end_time".

    2. --output_dir: path to the output directory.
    -------------------------------------
    !!!!! please use absolute path. !!!!!
    -------------------------------------

        e.g. --output_dir= "/data/youtube_data"
            --output_dir= "/data/youtube_data/" will not work.

        The downloaded audios will be stored in folder specified by this argument, 
        their filenames are the same as the ids in the csv file, such as 
        4kJVb8tPZmw.flac. The folder will be created if it does not exist. 

    3. --cpus: number of cpus to use.
        e.g. --cpus 4

    4. --json_file: if True, the downloaded metadata will be stored in a json file
    at the directory specified by --output_dir.
        e.g. --json_file True 
        e.g. file name: 4kJVb8tPZmw.json



requirements:
    - yt_dlp
    - ffmpeg installed in the system
    - pandas
    - audio_utils and file_utils
"""
from __future__ import unicode_literals
from multiprocessing import Pool
import yt_dlp
import pandas as pd
import functools as ft
from file_utils import json_dump
import audio_utils as au
import os
import argparse




def generate_URL(ids):
    """ generate_URL
    Args:
        ids (List[Str]): List of youtube IDs.

    Returns:
        List[Str]: List of youtube Links 
    """

    return list(map(lambda id: f"https://www.youtube.com/watch?v={id}",ids)) 


def download_from_URL(URL, output_dir, json_file):
    """ Use yt-pld package API to download.
    Args:
        URL (str): literal meaning 
        output_dir (str): literal meaning
    """
    ydl_opts = {
        "outtmpl": output_dir +"/temp"+"%(id)s.%(ext)s", 
        # since ffmpeg can not edit file in place, input and output file name can not be the same
        "format": "bestaudio/best",
        "postprocessors": [
            {   
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav"
            },
        ]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
        if json_file:
            info = ydl.extract_info(URL, download=False)
            id = info["id"]
            # store all metadatas available from youtube page:
            # ydl.sanitize_info makes the info json-serializable
            json_dump(ydl.sanitize_info(info), f"{output_dir}/{id}.json")


def download_multi_process(csv_path, output_path, num_cores, json_file = False):
    """ 
    Function: Read a csv files indicated by {csv_path} and download videos from youtube links
    in parallel, and save to the folder specified by output_path. The csv file must contain 
    a column of youtube IDs named "id". If the csv file contains also 2 columns named "start_time" and
    "end_time", the videos will be downloaded and the only the part between the start_time 
    and end_time will be kept. Final result is a folder of .flac files with sampling rate of 48KHZ,
    and json files for each audio by demand. 

    csv file format:

    id,start_time,end_time,...
    4kJVb8tPZmw,0,10,...
    ...

    or:

    id,...,...
    4kJVb8tPZmw,...,...
    ....

    !!! Attention: start_time and end_time are in seconds.


    Args:
        input_path (str):  literal meaning
        output_path (str): literal meaning 
        num_cores (int): number of processors to use (while downloading and processing) 
        json_file (bool, optional): Whether or not save metadata to json file. 
            Defaults to False.
    """
    # get youtube ids
    df = pd.read_csv(csv_path)
    try:
        ids = df.loc[:,"id"].tolist()
    except KeyError:
        raise KeyError("The csv file must contain a column named 'id'")

    #transform the ids to youtube links
    URLs = generate_URL(ids)
    #download the audios  
    with Pool(num_cores) as p:
        temp = ft.partial(download_from_URL,output_dir = output_path, json_file = json_file)
        p.map(temp,URLs) 
    # juge if start_time and end_time are in the csv file
    cut_necessary = False
    try:
        start_times = df.loc[:,"start_time"].tolist()
        end_times = df.loc[:,"end_time"].tolist()
        cut_necessary = True
    except KeyError:
        pass

    # cut audios, transform to .flac and change the sampling rate 
    global cut_process_audio
    def cut_process_audio(tuple):
        id = tuple[0]
        start= tuple[1]
        end= tuple[2]
        # convert to flac (sampling rate will be set in au.audio_to_flac)
        au.audio_to_flac(f"{output_path}/temp{id}.wav", f"{output_path}/temp{id}.flac")
        os.remove(f"{output_path}/temp{id}.wav")
        # cut the audio
        au.cut_audio(f"{output_path}/temp{id}.flac",f"{output_path}/{id}.flac", start, end)
        os.remove(f"{output_path}/temp{id}.flac")

    global just_process_audio
    def just_process_audio(id):
        au.audio_to_flac(f"{output_path}/temp{id}.wav", f"{output_path}/{id}.flac")
        os.remove(f"{output_path}/temp{id}.wav")


    with Pool(num_cores) as p:
        if cut_necessary:
            tuples =zip(ids, start_times, end_times)
            p.map(cut_process_audio,tuples)
        else:
            p.map(just_process_audio,ids) 

    print("--------------------------------------------------------")
    print("- All audios in csv file are dowloaded and processed!  -")
    print("--------------------------------------------------------")



if __name__ == "__main__": 

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv_path",
        type=str,
        help="input csv file path, example: ./data/example.csv"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="output path, where the downloaded files will be stored. Please use absolute path."
    )
    parser.add_argument(
        "--cpu_num",
        type=str,
        help="Number of cpu to use for downloading and converting. This script support multiprocessing."
    )
    parser.add_argument(
        "--json_file",
        type=str,
        help="Can be True of False. Whether or not to save metadata of a video to a json file. Optional."
    )


    args = parser.parse_args()
    if args.json_file == "True":
        json_file = True
    elif args.json_file == "False":
        json_file = False

    download_multi_process(args.csv_path, args.output_dir, int(args.cpu_num), args.json_file)


