'''
This python script creates a file
for each genre, and in it there will be 
the total number of songs and 
the number of songs per artist
'''

import pathlib 
import csv

# maps artist names to their song count #
songs = dict()

# total number of songs for genre #
total = 0

'''
Get all csv files in directory 
'''
p = pathlib.Path('.')
song_files = list(p.glob('*.csv'))

'''
open every file and 
get number of songs 
'''
for song_file in song_files :
  artist = song_file.name[:-4]
  
  # open file #
  fp = open(song_file.name, 'r', newline='')
  reader = csv.reader(fp, delimiter=',')

  # read number of songs on file #
  song_count = 0
  for row in reader :
    if row[0] == "" :
      break
    song_count += 1
  
  # save song count #
  songs[artist] = song_count 
  total += song_count

  # close file #
  fp.close()


'''
Save results on a file
for that genre 
'''
results = open("rock_count.csv", 'w', newline='')
writer = csv.writer(results, delimiter=',')

# write header #
header = ["Total", total]
writer.writerow(header)

# write rest of dictionary content #
for artist, count in songs.items() :
  row = [artist, count]
  writer.writerow(row)

# close files #
results.close()
