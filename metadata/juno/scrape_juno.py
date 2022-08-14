import bs4
import requests
import jsonlines
from urllib import parse


def get_items(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all(class_='dv-item')
    next_page = soup.find('a', title='Next Page')
    if next_page:
        next_page_url = next_page['href']
    else:
        next_page_url = None
    return items, next_page_url


def parse_item(item):
    text_fields = item.find_all(class_='vi-text mb-1')
    artist_links = text_fields[0].find_all('a', class_='text-md')
    artists = [parse.unquote(link['href'].split('/')[-2].replace('+', ' ')) for link in artist_links]
    album = text_fields[1].find('a').text
    track_link_list = item.find('ol')
    if track_link_list:
        track_links = track_link_list.find_all('a')
        track_urls = [track_link['href'] for track_link in track_links]
        track_titles = [title_div.text.strip() for title_div in track_link_list.find_all('div', class_='vi-text')]
    else:
        track_urls = []
        track_titles = []
    genre = item.find_all(class_='vi-text mb-2')[1].text
    review = item.find(class_='dvi-sales-notes')
    review = review.find('div').text.replace('Review:', '').strip() if review else ''
    return {
        'artists': artists,
        'album': album,
        'track_urls': track_urls,
        'track_titles': track_titles,
        'genre': genre,
        'review': review
    }


if __name__ == "__main__":
    start_url = 'https://www.juno.co.uk/all/back-cat/?facet%5Bclass_string%5D%5B%5D=album&facet%5Bclass_string%5D%5B%5D=single'
    items, next_page = get_items(start_url)
    parsed_data = []
    page_count = 0
    for item in items:
        parsed_data.append(parse_item(item))
    while next_page:
        print(page_count)
        page_count += 1
        items, next_page = get_items(next_page)
        for item in items:
            parsed_data.append(parse_item(item))

    with jsonlines.open('juno_tracks.jsonl', 'w') as writer:
        writer.write_all(parsed_data)
