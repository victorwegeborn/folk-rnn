import sys
import argparse
import re
import json

#### Configurations ####

## Different meters and lengths can have 
## different groupings of bars and notes
## Add to the dictionary the exact apperance
## of the meter/length and then (notes,bars)

## Example:
## For 'M:4/2' you want every 7 bar to create 
## a new line, and group notes in pairs of three:
## 'M:4/2' : (3,7),
## !!! Meter is prioritized over length !!!
## The default is 2 notes in every pair
## and 4 bars per line

## Also be aware that this only applies to the 
## meter and length that appears in the song header
## not for changes in the song

configurations = {
        'default': (2,4),
        }

#### End configurations ####

def format_notes(note_string,notes_group_size,bars_group_size):
    tokens = note_string.split(' ')
    #Right now, we only care about matching notes and bars
    re_note = re.compile(r"\^{0,2}\_{0,2}=?[A-Ga-g]'?,?")
    re_bar = re.compile(r":?\|:?")

    current_size_notes = 0
    current_size_bars = 0
    current_line_count = 0

    clean_notes = ['']
    for token in tokens:
        if token == '':
            continue
        elif re_note.match(token):
            #check if we need space
            if current_size_notes >= notes_group_size:
                #we need a space
                clean_notes[current_line_count] += ' '
                current_size_notes = 0
            #append it
            clean_notes[current_line_count] += token
            current_size_notes += 1
        elif re_bar.match(token):
            clean_notes[current_line_count] += token
            current_size_bars += 1
            #A bar also resets note count
            current_size_notes = 0
            if current_size_bars > bars_group_size:
                #Just so we dont hit a bad index
                clean_notes.append('')
                current_line_count += 1
                current_size_bars = 0
        else:
            clean_notes[current_line_count] += token
    return clean_notes

def format_song(song):
    song = song.strip().split("\n")
    if len(song) != 4:
        return None
    clean_song = []
    #first line should be fine with an X
    clean_song.append(song[0])
    #second and third line needs to remove brackets
    for i in range(1,3):
        clean_song.append(song[i][1:-1])
    #Now the real work
    #filter out key (if there is one)
    if song[3][:2] == '[K':
        index_end_key = song[3].find(']')
        key = song[3][1:index_end_key]
        clean_song.append(key)
        song[3] = song[3][index_end_key + 1:]
    # Fetch the default bars/notes conf
    (group_notes_size,group_bars_size) = configurations['default']
    # Check grouping
    # Clean song 1 == Length
    if configurations.get(clean_song[1]):
        (group_notes_size,group_bars_size) = configurations[clean_song[1]]
    #Clean song 2 == Meter
    if configurations.get(clean_song[2]):
        (group_notes_size,group_bars_size) = configurations[clean_song[2]]

    clean_notes = format_notes(song[3], group_notes_size, group_bars_size)
    clean_song.extend(clean_notes)
    # add a new line inbetween songs
    clean_song.append('')
    return '\n'.join(clean_song)

def read_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    return lines

def split_into_songs(lines):
    one_string = ''.join(lines)
    songs = one_string.split('\n\n')
    return songs

def main(filename):
    lines = read_file(filename)
    songs = split_into_songs(lines)
    for song in songs:
        formatted_song = format_song(song)
        if formatted_song is None:
            continue
        print formatted_song.strip()
        # newline between songs
        print ""
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: formatter.py <file to format>"
        sys.exit(1)
    main(sys.argv[1])
