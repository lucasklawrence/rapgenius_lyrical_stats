# Rap Genius Lyrical Word Cloud

This project uses the rap genius api to search for an artist and then scrape through that artist's different albums and songs to create a word cloud and display certain stats about the words in each album and the artist's discography

## Stats Tracked:
* Count of each word
* Count of starting letter of each word
* Average length of word
* Number of unique words
* Average length of unique words

The same stats are also tracked with the following words removed. I believe this provides Word Clouds that are more interesting.

##### Removed pronouns
"i", "me", "my", "mine", "myself",
"you", "your", "yours", "yourself",
"he", "him", "his", "himself",
"she", "her", "hers", "herself",
"it", "its", "itself",
"we", "us", "our", "ours", "ourselves",
"they", "them", "their", "theirs",

##### Removed articles
"a", "the", "an",
##### Removed prepositions
"at", "in", "by", "for", "on", "to", "from", "of", "with"

The goal of this project is to have an application that can produce the word clouds along with the stats for each word cloud on a single page

### Example Run of Program
```
Enter an artist to search for on rap genius: zhu
1: https://genius.com/artists/Zhu-and-alunageorge
2: https://genius.com/artists/Zhu-skrillex-and-they
3: https://genius.com/artists/Zhu-a-trak-and-keznamdi
4: https://genius.com/artists/Zhu
5: Search for new artist
Select the correct rap genius url for the artist: 4
Scraping lyrics for album: ringos desert pt 1
Finished in: 4.208654 seconds
Scraping lyrics for album: generationwhy
Finished in: 6.466686 seconds
Scraping lyrics for album: stardustexhalemarrakechdreams
Finished in: 2.873978 seconds
Scraping lyrics for album: my life remixes
Finished in: 3.524245 seconds
Scraping lyrics for album: ringos desert
Finished in: 4.718551 seconds
Scraping lyrics for album: genesis series
Finished in: 4.310134 seconds
A: Zhu Word Cloud
1: Album "ringos desert pt 1" word cloud
2: Album "generationwhy" word cloud
3: Album "stardustexhalemarrakechdreams" word cloud
4: Album "my life remixes" word cloud
5: Album "ringos desert" word cloud
6: Album "genesis series" word cloud
7: Search for new artist
8: End program
Select a Word Cloud to display: A
Select a Word Cloud to display:
Input was not one of the valid choices
Select a Word Cloud to display: 7
Enter an artist to search for on rap genius: em
1: https://genius.com/artists/2pac
2: https://genius.com/artists/Eminem
3: Search for new artist
Select the correct rap genius url for the artist: 2
Scraping lyrics for album: the eminem show
Finished in: 9.332515 seconds
Scraping lyrics for album: the slim shady lp
Finished in: 14.595006 seconds
Scraping lyrics for album: the singles
Finished in: 6.649954 seconds
Scraping lyrics for album: curtain call the hits
Finished in: 8.198473 seconds
Scraping lyrics for album: the marshall mathers lp 2
Finished in: 10.929083 seconds
Scraping lyrics for album: music from and inspired by the motion picture 8 mile
Finished in: 11.495558 seconds
Scraping lyrics for album: recovery
Finished in: 10.184538 seconds
Scraping lyrics for album: the marshall mathers lp
Finished in: 8.199192 seconds
Scraping lyrics for album: the marshall mathers lp2
Finished in: 5.2121 seconds
Scraping lyrics for album: kamikaze
Finished in: 7.496403 seconds
Scraping lyrics for album: relapse refill
Finished in: 13.258293 seconds
A: Eminem Word Cloud
1: Album "the eminem show" word cloud
2: Album "the slim shady lp" word cloud
3: Album "the singles" word cloud
4: Album "curtain call the hits" word cloud
5: Album "the marshall mathers lp 2" word cloud
6: Album "music from and inspired by the motion picture 8 mile" word cloud
7: Album "recovery" word cloud
8: Album "the marshall mathers lp" word cloud
9: Album "the marshall mathers lp2" word cloud
10: Album "kamikaze" word cloud
11: Album "relapse refill" word cloud
12: Search for new artist
13: End program
Select a Word Cloud to display: A
Select a Word Cloud to display: 13

Process finished with exit code 0
```
