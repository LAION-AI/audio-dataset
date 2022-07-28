import requests
import os
from bs4 import BeautifulSoup
import unicodedata
import re
import pandas as pd
import time


USER_NAME = 'yuchen22314'
USER_PASSWORD = '7reN9mHQJ#9WN.j'


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def get_tokens_session_id():
    r = requests.get('https://freesound.org/home/login')
    csrf_token = str(
        r.headers['set-cookie'].partition("csrftoken=")[2].partition(";")[0])
    getpage_soup = BeautifulSoup(r.text, 'xml')
    csrf_middleware_token = str(getpage_soup.find(
        'input', attrs={'name': 'csrfmiddlewaretoken'}).get_attribute_list('value')[0])
    del getpage_soup

    cookies = {'cookieConsent': 'yes', 'csrftoken': csrf_token}
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Opera GX";v="85"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://freesound.org',
        'Referer': 'https://freesound.org/home/login/?next=/',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }
    data = {
        'csrfmiddlewaretoken': csrf_middleware_token,
        'username': USER_NAME,
        'password': USER_PASSWORD,
        'next': '/',
    }
    response = requests.post(
        'https://freesound.org/home/login/', cookies=cookies, headers=headers, data=data)
    session_id = str(str(response.request.headers).partition(
        "sessionid=")[2].partition("'")[0])
    return csrf_token, csrf_middleware_token, session_id


def download_getter(csrf_token, csrf_middleware_token, session_id, sound_username, sound_id, sound_title):
    cookies = {
        'csrftoken': csrf_token,
        'sessionid': session_id,
    }
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Opera GX";v="85"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.79',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://freesound.org/',
        'Accept-Language': 'en-GB,en;q=0.9'
    }
    data = {
        'csrfmiddlewaretoken': str(csrf_middleware_token),
        'username': USER_NAME,
        'password': USER_PASSWORD,
        'next': '/',
    }

    response = requests.post(
        f'https://freesound.org/people/{sound_username}/sounds/{sound_id}/download/{sound_id}__{sound_username.lower()}__{sound_title}', cookies=cookies, headers=headers, data=data)

    # sterilisation of the file name
    first_part = os.path.basename(response.url).partition(".")[0]
    second_part = os.path.basename(response.url).partition(".")[2]
    filename = str(slugify(first_part) + "." + second_part)
    return response, filename


def download_sound(csrf_token, csrf_middleware_token, session_id, sound_username, sound_id, sound_title, folder):
    start = time.time()
    response, filename = download_getter(
        csrf_token, csrf_middleware_token, session_id, sound_username, sound_id, sound_title)
    with open(str(folder + '/' + filename), "wb") as f:
        f.write(response.content)
    print(f"Downloaded {filename} in {time.time() - start} seconds")
    del response, filename


csrf_token, csrf_middleware_token, session_id = get_tokens_session_id()
sets = "./parquet" 
save_folder = "./" 
for file in os.listdir(sets):
    df = pd.read_parquet(sets + '/' + file).head(100)
    for index, row in df.iterrows():
        download_sound(csrf_token, csrf_middleware_token, session_id,
                       row['username'], row['id'], row['title'], save_folder)