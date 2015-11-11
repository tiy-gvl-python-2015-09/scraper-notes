import requests
from bs4 import BeautifulSoup

index_url = "http://www.metrolyrics.com/queen-lyrics.html"
body = requests.get(index_url).content
souper = BeautifulSoup(body)
page_links = [link.attrs['href'] for link in souper.findAll('span', {'class': 'pages'})[0].findAll('a')]

for page in page_links:
    body = requests.get(page).content
    lyric_links = [link.attrs['href'] for link in souper.findAll('a', {'class': 'title'})]

    for lyric_page in lyric_links:
        body = requests.get(lyric_page).content
        souper = BeautifulSoup(body)
        target_div_id = "lyrics-body-text"
        if souper.find(id=target_div_id):
            print(souper.find(id=target_div_id).text)

"""
song_url = "http://www.metrolyrics.com/loser-lyrics-beck.html"
target_div_id = "lyrics-body-text"

print(souper.find(id=target_div_id).text)
"""
