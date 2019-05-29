from rauth import OAuth2Service
import http
import requests
from http import HTTPStatus
from bs4 import BeautifulSoup
import re
from artist import Artist, Album, Song
import wordcloud
import matplotlib.pyplot as plt
from collections import Counter


def find_artist_url(search_artist):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + '071qS0OFRPZ8HNpnv_D8XeVCIFJLxIoc287fimUGIlAKciRrQlDkaKUIvbH15p_C'}
    search_url = base_url + '/search'
    data = {'q': search_artist}
    response = requests.get(search_url, data=data, headers=headers)

    json = response.json()
    meta = json['meta']

    # verify http status was 200
    http_status = meta['status']
    if http_status != 200:
        raise ValueError('Http Status was incorrect')

    # find artist url

    response = json['response']
    hits = response['hits']
    possible_artist_urls = set()
    for hit in hits:
        result = hit['result']
        primary_artist = result['primary_artist']
        url = primary_artist['url']
        if url not in possible_artist_urls:
            possible_artist_urls.add(url)

    return possible_artist_urls


def get_artist_albums_from_artist_url(artist_link):
    html = requests.get(artist_link)
    data = html.text
    soup = BeautifulSoup(data, "html.parser")

    album_urls = set()
    for link in soup.find_all('a'):
        possible_link = link.get('href')
        if re.match('https://', possible_link) and re.search('albums', possible_link):
            if possible_link.lower() not in album_urls:
                album_urls.add(possible_link.lower())

    return album_urls


def get_song_urls_from_album_url(album_link):
    html = requests.get(album_link)
    data = html.text
    soup = BeautifulSoup(data, "html.parser")

    song_genius_urls = set()
    for link in soup.find_all('a'):
        possible_link = link.get('href')

        # this gets all possible songs from the album
        if re.search("-lyrics", possible_link):
            song_genius_url = possible_link.lower()
            if song_genius_url not in song_genius_urls:
                song_urls.add(song_url)

    return song_urls


def get_lyrics_from_song_url(song_link):
    html = requests.get(song_link)
    data = html.text
    soup = BeautifulSoup(data, "html.parser")

    lyrics_html = soup.find("div", {"class": "lyrics"})

    song_lyrics = None
    if lyrics_html is not None:
        song_lyrics = lyrics_html.get_text()

    return song_lyrics


if __name__ == '__main__':
    search_for = "Eminem"
    artist_urls = find_artist_url(search_for)
    artist_url = artist_urls.pop()
    artist = Artist(search_for, artist_url)

    # Get Albums from Artist
    album_urls = get_artist_albums_from_artist_url(artist.get_artist_url())

    # create albums for artist
    for album_url in album_urls:
        init_partition = str.partition(album_url, artist.get_artist_name().lower())
        album_name = (str.partition(init_partition[2], "/"))[2]
        album_name = str.replace(album_name, "-", " ")
        album = Album(album_name, album_url)
        artist.add_album(album)

    # create songs for album
    for album in artist.get_albums():
        song_urls = get_song_urls_from_album_url(album.get_album_url())
        for song_url in song_urls:
            song_title = (str.partition(song_url, "genius.com/"))[2]
            song = Song(song_title, song_url)
            song.set_lyrics(get_lyrics_from_song_url(song.get_song_url()))
            song.set_word_count_from_lyrics()
            album.add_song(song)
    flag = 0
    for album in artist.get_albums():
        album.set_word_count_from_songs()
        lyrics = ""
        for song in album.get_songs():
            if song.get_lyrics() is not None:
                lyrics += song.get_lyrics()
        words = lyrics.lower().split()
        wordCount = Counter(words)

    artist.set_word_count_from_albums()

    artist_word_cloud = wordcloud.WordCloud().generate_from_frequencies(artist.get_word_count())
    # Display the generated image:
    plt.imshow(artist_word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
