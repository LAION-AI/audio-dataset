from __future__ import unicode_literals
from multiprocessing import Pool
import yt_dlp
import pandas as pd
import functools as ft
from file_utils import json_dump
"""
This module contains auxiliary functions allowing us to download youtube videos
and transform then to .flac with sampling rate of 4800.

"""
def read_CSV(input_Path):
    pass


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
        URL (_type_): _description_
        output_dir (_type_): _description_
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

def download_multi_process(input_path, output_path, URLS, num_cores, json_file = False):
    """_summary_

    Args:
        input_path (str):  
        output_path (str): _description_df
        URLS (str): _description_
        num_cores (_type_): _description_
        json_file (bool, optional): _description_. Defaults to False.
    """
    p = Pool(num_cores)
    temp = ft.partial(download_from_URL,output_dir = output_path)
    p.map(temp,URLS) 
 

URLS = ["https://www.youtube.com/embed/4kJVb8tPZmw/start=10&end=30"]
download_from_URL("https://www.youtube.com/embed/4kJVb8tPZmw/start=10&end=30", "/home/yuchenhui/testvideo/")
#download_multi_process(None, "/home/yuchenhui/testvideo/" , URLS, 4)