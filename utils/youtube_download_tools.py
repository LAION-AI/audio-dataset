from __future__ import unicode_literals
from multiprocessing import Pool
import youtube_dl
import pandas as pd
'''
This module contains auxiliary functions allowing us to download youtube videos
and transform then to .flac with sampling rate of 4800.
'''

def read_CSV(input_Path):
    pass

def transform():
    pass

def generate_URL(ids,times):
    """ generate_URL
    Args:
        ids (List[Str]): list of youtube IDs.
        times (List[Tuple[]]): 
            List of start time and end time for each audio, unit is second. 
            example: [(30,40)]

    Returns:
        List[Str]:  
    """
    
    #prefix = "https://www.youtube.com/embed/" + 

    return URLS


def download_from_URL(URL, output_dir):
    '''
    th
    '''
    ydl_opts = {
        "outtmpl": output_dir + '%(title)s.%(ext)s',
        "format": "bestaudio/best",
        'postprocessors': [
            {   
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav'
            },
        ]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([URL])
        print(result)


# Note: Multiprocessing may be useless, 
# since download is an IO intensive task.
def download_multi_process(input_path, output_path, URLS, num_cores):
   p = Pool(num_cores)
   p.map(download_from_URL,URLS) 

download_from_URL("https://www.youtube.com/watch?v=4kJVb8tPZmw", "/home/yuchenhui/testvideo/")