"""
This module contains auxiliary functions allowing us to download youtube videos
and transform then to .flac with sampling rate of 4800.

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
        "outtmpl": output_dir + "%(id)s.%(ext)s",
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
        temp = ft.partial(download_from_URL,output_dir = output_path)
        p.map(temp,URLs) 
 
    # juge if start_time and end_time are in the csv file
    cut_necessary = False
    try:
        start_times = df.loc[:,"start_time"].tolist()
        end_times = df.loc[:,"end_time"].tolist()
        cut_necessary = True
    except KeyError:
        pass

    # (cut audios), transform to .flac and change the sampling rate 
    def cut_process_audio(id,start,end):
        if cut_necessary:
            # cut the audio
            au.cut_audio(f"{output_path}/{id}.wav", start, end)
        # convert to flac (sampling rate will be set in au.audio_to_flac)
        au.audio_to_flac(f"{output_path}/{id}.wav", f"{output_path}/{id}.flac")


    with Pool(num_cores) as p:
        p.map(cut_process_audio,zip(ids, start_times, end_times))

    print("--------------------------------------------------------")
    print("- All audios in csv file are dowloaded and processed!  -")
    print("--------------------------------------------------------")






URLS = ["https://www.youtube.com/embed/4kJVb8tPZmw/start=10&end=30"]
download_from_URL("https://www.youtube.com/embed/4kJVb8tPZmw/start=10&end=30", "/home/yuchenhui/testvideo/")
#download_multi_process(None, "/home/yuchenhui/testvideo/" , URLS, 4)