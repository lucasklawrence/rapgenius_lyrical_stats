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

def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + '071qS0OFRPZ8HNpnv_D8XeVCIFJLxIoc287fimUGIlAKciRrQlDkaKUIvbH15p_C'}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def find_artist_url(artist):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + '071qS0OFRPZ8HNpnv_D8XeVCIFJLxIoc287fimUGIlAKciRrQlDkaKUIvbH15p_C'}
    search_url = base_url + '/search'
    data = {'q': artist}
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
        artist = result['primary_artist']
        url = artist['url']
        if url not in possible_artist_urls:
            possible_artist_urls.add(url)

    return possible_artist_urls


def get_artist_albums_from_artist_url(artist_url):
    html = requests.get(artist_url)
    data = html.text
    soup = BeautifulSoup(data, "html.parser")

    album_urls = set()
    for link in soup.find_all('a'):
        possible_link = link.get('href')
        if re.match('https://', possible_link) and re.search('albums', possible_link):
            if possible_link.lower() not in album_urls:
                album_urls.add(possible_link.lower())

    return album_urls


def get_song_urls_from_album_url(album_url):
    html = requests.get(album_url)
    data = html.text
    soup = BeautifulSoup(data, "html.parser")

    song_urls = set()
    for link in soup.find_all('a'):
        possible_link = link.get('href')

        ## this gets all possible songs from the album
        if re.search("-lyrics", possible_link):
            song_url = possible_link.lower()
            if song_url not in song_urls:
                song_urls.add(song_url)

    return song_urls


def get_lyrics_from_song_url(song_url):
    html = requests.get(song_url)
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
        #sprint(album.get_word_count())
        lyrics = ""
        for song in album.get_songs():
            if song.get_lyrics() is not None:
                lyrics += song.get_lyrics()
        words = lyrics.lower().split()
        wordCount = Counter(words)
        #print(wordCount)

    artist.set_word_count_from_albums()

    artist_word_cloud = wordcloud.WordCloud().generate_from_frequencies(artist.get_word_count())
    # Display the generated image:
    plt.imshow(artist_word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    #print(artist.get_word_count())

"""
    flag = 0
    for link in test:
        albums = get_artist_albums_from_artist_url(link)
        for album in albums:
            album_songs = get_song_urls_from_album_url(album)
            for song in album_songs:
                if flag == 0:
                    get_lyrics_from_song_url(song)
                    flag = 1


# change the JSON string into a JSON object
#jsonObject = json.loads(json)

# print the keys and values
for key in json:
    value = json[key]
    for item in value:
        print(value[item])
    print("The key and value are ({}) = ({})".format(key, value))
remote_song_info = None

wow = requests.get('https://genius.com/search?q=', data='Drake')
print(wow.text)
#for hit in json['response']['hits']:
#    if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
#       remote_song_info = hit
#        break

print(remote_song_info)
#print(session)
#rap_genius.get_access_token()
#rap_genius.get_access_token(str='POST', decoder=parse_utf8_qsl, key=s)

#https://api.genius.com/oauth/authorize?
#client_id=YOUR_CLIENT_ID&
#redirect_uri=YOUR_REDIRECT_URI&
#scope=REQUESTED_SCOPE&
#state=SOME_STATE_VALUE&
#response_type=code

#print(request_token)
"""