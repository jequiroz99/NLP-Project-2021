'''
This python script creates a CSV file named 
'artists.csv' which contains the name and genre
of all artists that appear in both datasets.
This means that we know the genre of the artist 
and we also have song lyrics for that artist!
'''
import csv

f = dict()
g = dict()

'''
# dictionary that maps artist (str) to TOTAL number of songs (int)
songs = dict()

# dictionary that maps genre (str) to a list of artists that appear in that genre (list)
artists = dict()
'''

# open 'artists-data' file #
file1 = open('artists-data.csv', 'r')
artists_data = csv.reader(file1, delimiter=',')

# open 'lyrics-data' file #
file2 = open('lyrics-data.csv', 'r')
lyrics_data = csv.reader(file2, delimiter=',')

# valid genres, meaning that we will only predict
# from this genres 
valid = ['Rock', 'Pop', 'Hip Hop']

# read header of both files #
header = next(artists_data)
header = next(lyrics_data)

'''
Read the artists-data file 
'''
for line in artists_data :
  
  # save artist and genre in dict f #
  genre = line[4]
  artist = line[0].lower()
  if not artist in f :
    f[artist] = genre
  
'''
Read the lyrics-data file
'''
for line in lyrics_data :

  # save artist and number of english songs in dict g #
  artist = line[0].replace("/", "").replace("-", " ")
  if not artist in g :
    g[artist] = 0

  if line[4] == "ENGLISH" :
    g[artist] += 1

'''
Save artist names that appear in both datasets
AND have english songs
'''
artists = list(f.keys())
for artist in artists:
  if artist in g and g[artist] > 0 and f[artist] in valid:  
    print(f'{artist},{f[artist]}')

'''
Close readers and exit gracefully
'''
file1.close()
file2.close()
