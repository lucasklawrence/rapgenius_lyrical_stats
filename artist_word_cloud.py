from rauth import OAuth2Service
import http
import requests
from http import HTTPStatus
from bs4 import BeautifulSoup
import re
from artist import Artist, Album, Song
import string

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
                song_genius_urls.add(song_genius_url)

    return song_genius_urls


def get_lyrics_from_song_url(song_link):
    html = requests.get(song_link)
    data = html.text
    soup = BeautifulSoup(data, "html.parser")
    lyrics_html = soup.find("div", {"class": "lyrics"})

    song_lyrics = None
    if lyrics_html is not None:
        song_lyrics = lyrics_html.get_text()

    # remove [Chorus: Artist 1] [Verse: Artist 2], etc
    song_lyrics = remove_items_in_brackets(song_lyrics)
    # removes punctuation
    song_lyrics = song_lyrics.translate(str.maketrans('', '', string.punctuation))
    return song_lyrics


def remove_items_in_brackets(lyrics):
    initial_indices = list()
    end_indices = list()

    # get starting and ending points of brackets in string
    for i in range(len(lyrics)):
        if lyrics[i] == '[':
            initial_indices.append(i)
        if lyrics[i] == ']':
            end_indices.append(i)

    initial_length = len(initial_indices)
    end_length = len(end_indices)
    remove = list()

    # get strings that are in brackets to replace with empty strings
    if initial_length == end_length:
        for i in range(initial_length):
            initial_index = initial_indices[i]
            end_index = end_indices[i]
            remove.append(lyrics[initial_index:end_index + 1])

    # replace strings w/ empty string
    for item in remove:
        lyrics = lyrics.replace(item, "")

    return lyrics


def add_albums_to_artist(artist):
    # Get Albums from Artist
    genius_album_urls = get_artist_albums_from_artist_url(artist.get_artist_url())

    # create albums for artist
    for genius_album_url in genius_album_urls:
        init_partition = str.partition(genius_album_url, artist.get_artist_name().lower())
        album_name = (str.partition(init_partition[2], "/"))[2]
        album_name = str.replace(album_name, "-", " ")
        album = Album(album_name, genius_album_url)
        artist.add_album(album)


def add_songs_to_artist_albums(artist):
    # create songs for album
    for album_iter in eminem.get_albums():
        song_urls = get_song_urls_from_album_url(album_iter.get_album_url())
        for song_url in song_urls:
            song_title = (str.partition(song_url, "genius.com/"))[2]
            current_song = Song(song_title, song_url)
            current_song.set_lyrics(get_lyrics_from_song_url(current_song.get_song_url()))
            current_song.set_word_count_from_lyrics()
            album_iter.add_song(current_song)
        album_iter.set_word_count_from_songs()
    artist.set_word_count_from_albums()


if __name__ == '__main__':
    search_for = "Eminem"
    artist_urls = find_artist_url(search_for)
    artist_url = artist_urls.pop()
    eminem = Artist(search_for, artist_url)

    add_albums_to_artist(eminem)
    add_songs_to_artist_albums(eminem)

    artist_word_cloud = wordcloud.WordCloud().generate_from_frequencies(eminem.get_word_count())
    # Display the generated image:
    plt.imshow(artist_word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

