# web imports
import requests
from bs4 import BeautifulSoup

# regular expression and string to find lyrics / parts of lyrics
import re
import string

# import classes
from artist import Artist, Album, Song

# wordcloud and plot wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# datetime to print time for each album
import datetime as datetime


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
    for index in range(len(lyrics)):
        if lyrics[index] == '[':
            initial_indices.append(index)
        if lyrics[index] == ']':
            end_indices.append(index)

    initial_length = len(initial_indices)
    end_length = len(end_indices)
    remove = list()

    # get strings that are in brackets to replace with empty strings
    if initial_length == end_length:
        for index in range(initial_length):
            initial_index = initial_indices[index]
            end_index = end_indices[index]
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
        init_partition = str.partition(genius_album_url, "/albums/")
        album_name = (str.partition(init_partition[2], "/"))[2]
        album_name = str.replace(album_name, "-", " ")
        genius_album = Album(album_name, genius_album_url)
        artist.add_album(genius_album)


def add_songs_to_artist_albums(artist):
    # create songs for album
    for album_iter in artist.get_albums():
        song_urls = get_song_urls_from_album_url(album_iter.get_album_url())
        print("Scraping lyrics for album: " + album_iter.get_album_name())
        initial_time = datetime.datetime.now()
        for song_url in song_urls:
            song_title = (str.partition(song_url, "genius.com/"))[2]
            current_song = Song(song_title, song_url)
            current_song.set_lyrics(get_lyrics_from_song_url(current_song.get_song_url()))
            current_song.set_word_count_from_lyrics()
            album_iter.add_song(current_song)
        album_iter.set_word_count_from_songs()
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - initial_time).total_seconds()
        print("Finished in: " + str(elapsed_time) + " seconds")
    artist.set_word_count_from_albums()


def initialize_albums_and_songs(artist):
    add_albums_to_artist(artist)
    add_songs_to_artist_albums(artist)


def create_word_clouds_for_artist(artist):

    # set overall word cloud for artist
    if artist.get_word_count() is None:
        print("not initialize")

    if artist.get_word_count() is not None:
        artist_word_cloud = WordCloud().generate_from_frequencies(artist.get_word_count())
        artist.set_word_cloud(artist_word_cloud)

    # set word clouds for each album

    for artist_album in artist.get_albums():
        album_word_count = artist_album.get_word_count()
        album_word_cloud = WordCloud().generate_from_frequencies(album_word_count)
        artist_album.set_word_cloud(album_word_cloud)


if __name__ == '__main__':

    while True:
        search_for = input("Enter an artist to search for on rap genius: ")
        artist_urls = find_artist_url(search_for)
        choice = 1
        for url in artist_urls:
            print(str(choice) + ": " + url)
            choice = choice + 1

        choice = input("Select the correct rap genius url for the artist: ")
        choice_number = int(choice)
        artist_url = None
        for i in range(choice_number):
            artist_url = artist_urls.pop()
        if artist_url is not None:
            artist_name = str.partition(artist_url, "/artists/")[2]
            rap_genius_artist = Artist(artist_name, artist_url)

            initialize_albums_and_songs(rap_genius_artist)
            create_word_clouds_for_artist(rap_genius_artist)

            # print out choices and ask user to select which word cloud to present
            print("A: " + rap_genius_artist.get_artist_name() + " Word Cloud")
            choice = 1
            for album in rap_genius_artist.get_albums():
                print(str(choice) + ": Album \"" + album.get_album_name() + "\" word cloud")
                choice = choice + 1

            new_artist_choice = choice
            print(str(choice) + ": Search for new artist")
            end_choice = choice + 1
            print(str(end_choice) + ": End program")
            next_choice = None
            choice_number = 0

            while True:
                next_choice = input("Select a Word Cloud to display: ")
                if next_choice == 'A':
                    plt.imshow(rap_genius_artist.get_word_cloud(), interpolation='bilinear')
                    plt.title(rap_genius_artist.get_artist_name())
                    plt.axis("off")
                    plt.show()
                else:
                    choice_number = int(next_choice)
                    if choice_number == new_artist_choice or choice_number == end_choice:
                        break
                    i = 1
                    for album in rap_genius_artist.get_albums():
                        if choice_number == i:
                            plt.imshow(album.get_word_cloud(), interpolation='bilinear')
                            plt.title(album.get_album_name())
                            plt.axis("off")
                            plt.show()
                        i = i+1
            if choice_number == end_choice:
                break


