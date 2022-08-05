import jsonlines
import csv
import sys

if __name__ == "__main__":
    source = sys.argv[1]
    target = sys.argv[2]
    with jsonlines.open(source) as reader:
        data = list(reader)

    header = ['artists', 'album', 'genre', 'review', 'track_title', 'track_url']
    rows = []
    for item in data:
        artists = '|'.join(item['artists'])
        for track_title, track_url in zip(item['track_titles'], item['track_urls']):
            rows.append(
                [artists, item['album'], item['genre'], item['review'], track_title, track_url]
            )

    with open(target, 'wt') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=';')
        csv_writer.writerow(header)
        csv_writer.writerows(rows)
