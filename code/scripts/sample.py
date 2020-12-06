import csv

# dictionary that maps genres (str) to number of artists with that genre (int)
genres = dict()

# dictionay that maps artist (str) to number of songs in ENGLISH (int)
english = dict()

# dictionary that maps artist (str) to TOTAL number of songs (int)
songs = dict()

# dictionary that maps genre (str) to a list of artists that appear in that genre (list)
artists = dict()

# open 'artists-data' file #
file1 = open('artists-data.csv', 'r')
artists_data = csv.reader(file1, delimiter=',')

# open 'lyrics-data' file #
file2 = open('lyrics-data.csv', 'r')
lyrics_data = csv.reader(file2, delimiter=',')

# read header of both files #
header = next(artists_data)
header = next(lyrics_data)

'''
Read the artists-data file 
'''
for line in artists_data :
  # count occurence of genre in genre dict
  genre = line[4]
  if not genre in genres :
    genres[genre] = 0

  #genres[genre] += 1
  
  # save artist in artists dict #
  if not genre in artists :
    artists[genre] = list()
  
  artist = line[0].lower()
  artists[genre].append(artist)

'''
Read the lyrics-data file
'''
for line in lyrics_data :
  # Count number of songs of artist #
  artist = line[0].replace("/", "").replace("-", " ")
  if not artist in songs :
    songs[artist] = 0

  songs[artist] += 1

  # check if song is in english #
  if not artist in english :
    english[artist] = 0

  if line[4] == "ENGLISH" :
    english[artist] += 1


'''
Count number of english songs for each genre
'''
for genre, group in artists.items() :
  for artist in group :
    genres[genre] += english[artist]

'''
Print Results for english songs per artist
for artist, numSongs in songs.items() :
  print(f'Artist: {artist}\tEnglish:{english[artist]:d}/{numSongs:d}')
'''

'''
Print results for english song in each genre
'''
for genre, count in genres.items():
  print(f'{genre} has {count:d} english songs')

'''
Close readers and exit gracefully
'''
file1.close()
file2.close()
