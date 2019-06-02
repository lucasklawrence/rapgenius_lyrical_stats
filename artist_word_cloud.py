# web imports
import requests

# import classes
from artist import Artist, Album, Song, Stats

# wordcloud and plot wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def find_artist_url(search_artist):
    """

    :param search_artist: artist to search for
    :return: possible rap genius artist urls from search term
    """
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


def create_word_clouds_for_artist(artist):
    """

    :param artist: artist object to create word clouds from
    :return: sets the word clouds for the artist passed in
    """
    artist_word_count = artist.get_stats().get_word_count()
    artist_word_count_minus = artist.get_stats().get_word_count_minus()
    if len(artist_word_count) != 0:
        artist_word_cloud = WordCloud().generate_from_frequencies(artist_word_count)
        artist.set_word_cloud(artist_word_cloud)

    if len(artist_word_count_minus) != 0:
        artist_word_cloud_minus = WordCloud().generate_from_frequencies(artist_word_count_minus)
        artist.set_word_cloud_minus(artist_word_cloud_minus)

    # set word clouds for each album
    for artist_album in artist.get_albums():
        album_word_count = artist_album.get_stats().get_word_count()
        album_word_count_minus = artist_album.get_stats().get_word_count_minus()
        if len(album_word_count) != 0:
            album_word_cloud = WordCloud().generate_from_frequencies(album_word_count)
            artist_album.set_word_cloud(album_word_cloud)
        if len(album_word_count_minus) != 0:
            album_word_cloud_minus = WordCloud().generate_from_frequencies(album_word_count_minus)
            artist_album.set_word_cloud_minus(album_word_cloud_minus)


if __name__ == '__main__':

    while True:
        search_for = input("Enter an artist to search for on rap genius: ")
        artist_urls = find_artist_url(search_for)
        choice = 1
        for url in artist_urls:
            print(str(choice) + ": " + url)
            choice = choice + 1
        new_search_choice = choice
        print(str(new_search_choice) + ": Search for new artist")

        choice_input = input("Select the correct rap genius url for the artist: ")
        while not str.isdigit(choice_input) or int(choice_input) > choice:
            print("Input was not one of the valid choices")
            choice_input = input("Select the correct rap genius url for the artist: ")

        if int(choice_input) == new_search_choice:
            continue
        artist_url = None
        for i in range(int(choice_input)):
            artist_url = artist_urls.pop()
        if artist_url is not None:
            artist_name = str.partition(artist_url, "/artists/")[2]
            rap_genius_artist = Artist(artist_name, artist_url)

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
                while next_choice != 'A' and (not str.isdigit(next_choice) or int(next_choice) > end_choice):
                    print("Input was not one of the valid choices")
                    next_choice = input("Select a Word Cloud to display: ")

                if next_choice == 'A':
                    plt.imshow(rap_genius_artist.get_word_cloud_minus(), interpolation='bilinear')
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


