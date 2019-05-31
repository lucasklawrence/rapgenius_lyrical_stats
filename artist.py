
class Artist:
    def __init__(self, artist_name, artist_url):
        self.artist_name = artist_name
        self.artist_url = artist_url
        self.albums = list()
        self.wordCount = {}
        self.wordCloud = None

    def get_artist_name(self):
        return self.artist_name

    def set_artist_name(self, artist_name):
        self.artist_name = artist_name

    def get_artist_url(self):
        return self.artist_url

    def set_artist_url(self, artist_url):
        self.artist_url = artist_url

    def get_albums(self):
        return self.albums

    def add_album(self, album):
        self.albums.append(album)

    def get_word_count(self):
        return self.wordCount

    def set_word_count_from_albums(self):
        for album in self.get_albums():
            if album.get_word_count() is None:
                album.set_word_count_from_songs()

            for key in album.wordCount:
                if key not in self.wordCount:
                    self.wordCount[key] = album.wordCount[key]
                else:
                    previous_count = self.wordCount[key]
                    self.wordCount[key] = previous_count + album.wordCount[key]

    def get_word_cloud(self):
        return self.wordCloud

    def set_word_cloud(self, wordcloud):
        self.wordCloud = wordcloud


class Album:
    def __init__(self, album_name, album_url):
        self.album_name = album_name
        self.album_url = album_url
        self.songs = list()
        self.wordCount = {}
        self.wordCloud = None

    def get_album_name(self):
        return self.album_name

    def set_album_name(self, album_name):
        self.album_name = album_name

    def get_album_url(self):
        return self.album_url

    def set_album_url(self, album_url):
        self.album_url = album_url

    def get_songs(self):
        return self.songs

    def add_song(self, song):
        self.songs.append(song)

    def get_word_count(self):
        return self.wordCount

    def set_word_count_from_songs(self):
        for song in self.get_songs():
            if song.get_word_count() is None:
                song.set_word_count_from_lyrics()

            for key in song.wordCount:
                if key not in self.wordCount:
                    self.wordCount[key] = song.wordCount[key]
                else:
                    previous_count = self.wordCount[key]
                    self.wordCount[key] = previous_count + song.wordCount[key]

    def get_word_cloud(self):
        return self.wordCloud

    def set_word_cloud(self, wordcloud):
        self.wordCloud = wordcloud


class Song:
    def __init__(self, song_name, song_url):
        self.song_name = song_name
        self.song_url = song_url
        self.lyrics = None
        self.wordCount = {}

    def get_song_name(self):
        return self.song_name

    def set_song_name(self, song_name):
        self.song_name = song_name

    def get_song_url(self):
        return self.song_url

    def set_song_url(self, song_url):
        self.song_url = song_url

    def get_lyrics(self):
        return self.lyrics

    def set_lyrics(self, lyrics):
        self.lyrics = lyrics

    def get_word_count(self):
        return self.wordCount

    def set_word_count_from_lyrics(self):
        if self.lyrics is None:
            return

        words = self.lyrics.lower().split()
        for word in words:
            if word not in self.wordCount:
                self.wordCount[word] = 1
            else:
                prev_count = self.wordCount[word]
                self.wordCount[word] = prev_count + 1
