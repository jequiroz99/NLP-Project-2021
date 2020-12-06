'''
This python script will create 
a file for each artist named after
itself and will contain all of their song names 
and lyrics. The File will be placed in a folder 
named after the artist's genre.
'''
import csv

f = dict()
g = dict()

# dict that maps artist name to 
# a tuple of (song name, lyric)
dataset = dict()

# open 'artists.csv' file #
file1 = open('../artists.csv', 'r', newline='')
data = csv.reader(file1, delimiter=',')

# open 'lyrics-data' file #
file2 = open('../lyrics-data.csv', 'r', newline='')
lyrics_data = csv.reader(file2, delimiter=',')

# read header of file #
header = next(data)
header = next(lyrics_data)

'''
Read 'artists.csv' file
This will give us artist name and their genres!
'''
for line in data :
  
  # save artist and its main genre in dict f #
  artist = line[0]
  if not artist in f :
    f[artist] = line[1]
    dataset[artist] = list()

'''
Read the lyrics-data file
Save song name and lyric for each artist
'''
for line in lyrics_data :

  # get artist name, if it has a genre, then 
  # save the artist's song and lyrics in 'dataset' dict
  artist = line[0].replace("/", "").replace("-", " ")
  if artist in dataset and line[4] == "ENGLISH" :
    name = line[1].lower()
    lyrics = line[3]

    # save song name and lyrics #
    array = dataset[artist]
    array.append((name, lyrics))
    dataset[artist] = array
 

'''
For each artist, create a file named 
after the artist's name and in their
genre's folder
'''
artists = list(dataset.keys())
for artist in artists :
  
  # get genre of artist #
  genre = f[artist].lower()

  # create file #
  fname = genre + "/" + artist + ".csv"
  fp = open(fname, 'w', newline='')
  writer = csv.writer(fp)

  # write content to file #
  for item in dataset[artist] :
    row = [item[0], item[1]]
    writer.writerow(row)
  
  # close file #
  fp.close()

'''
Print Confirmation
'''
print('Done!')

'''
Close readers and exit gracefully
'''
file1.close()
file2.close()

