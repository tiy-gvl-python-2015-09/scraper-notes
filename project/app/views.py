from django.shortcuts import render, render_to_response
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup

from app.models import Song


def helloview(request):
    lyric_links = []
    if request.GET:
        body = requests.get("http://www.metrolyrics.com/{}-lyrics.html".format(request.GET.get('band').lower().replace(" ", "-"))).content
        souper = BeautifulSoup(body)
        page_link_object = souper.findAll('span', {'class': 'pages'})
        if page_link_object:
            page_links = [link.attrs['href'] for link in souper.findAll('span', {'class': 'pages'})[0].findAll('a')]
            for page in page_links:
                page_body = requests.get(page).content
                souper = BeautifulSoup(page_body)
                for link in souper.findAll('a', {'class': 'title'}):
                    lyric_links.append({"href": link.attrs['href'].replace('http://www.metrolyrics.com/', '').replace('.html', ''), "title": link.text.replace("Lyrics", "")})
        else:
            souper = BeautifulSoup(body)
            for link in souper.findAll('a', {'class': 'title'}):
                lyric_links.append({"href": link.attrs['href'].replace('http://www.metrolyrics.com/', '').replace('.html', ''), "title": link.text.replace("Lyrics", "")})


    return render_to_response('index.html', {"links": lyric_links})


def lyricview(request, song_title):
    song = Song.objects.filter(slug=song_title)
    if not song:
        print("going to metrolyrics")
        body = requests.get("http://www.metrolyrics.com/{}.html".format(song_title)).content
        souper = BeautifulSoup(body)
        target_div_id = "lyrics-body-text"
        lyric_body = ""
        if souper.find(id=target_div_id):
            lyric_body = souper.find(id=target_div_id).prettify
            song = Song.objects.create(title="", slug=song_title, body=lyric_body)
    else:
        lyric_body = song.first().body
        song = song.first()

    youtube_results = requests.get("https://www.youtube.com/results?search_query={}+karaoke".format(song.slug.replace("-", "+"))).content
    souper = BeautifulSoup(youtube_results)
    results = souper.findAll('ol', {'class': 'section-list'})[0].find('a')
    youtube_id = results.attrs['href'].replace("/watch?v=", "")
    return render_to_response('index.html', {"lyric_body": lyric_body, "youtube_id": youtube_id})
