import pandas as pd
import pickle

local_excel_file = 'C:/PyCharm/music_finder/test.xlsx'

camelots = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B', '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B', '11A', '11B', '12A', '12B']

# track class used throughout, contains metadata about a given track
class Track:
    def __init__(self, name, artist, camelot, tempo, genre):
        self.name = name
        self.artist = artist
        self.camelot = camelot
        self.tempo = tempo
        self.genre = genre

    def __repr__(self):
        return '{:50.50}{:50.50}{:5}{:<10}{:10}\t'.format(self.name, self.artist, self.camelot, self.tempo, self.genre)


# swaps letter (A or B) at end of camelot given
def get_relative_major_minor(camelot):
    if camelot[1] == 'A':
        return camelot[0] + 'B'
    else:
        return camelot[0] + 'A'


# given a track's title and artist, looks through older file versions to see if key has been found, returns it or N/A
def try_for_camelot(title, artist):
    df = pd.read_excel('file:C:/random/songs1.xlsx')
    for i, row in df.iterrows():
        if str(row['Title']).lower() in str(title.lower()) and str(row['Artist']).lower() in str(artist.lower()):
            return row['Camelot']
    return 'N/A'


# gets a simplistic form of the track's genre given the list of genres from the exportify file
def get_genre(input_genre):
    if 'rap' in input_genre.lower():
        return 'Rap'
    if 'edm' in input_genre.lower():
        return 'EDM'
    if 'pop' in input_genre.lower():
        return 'Pop'
    return 'Misc.'


# changes a key value from its alphanumeric value to a simply numeric one
def get_key_value(input_key):
    initial_value = int(input_key[0:1])
    if input_key[1:2] == 'A':
        return initial_value * 2
    if input_key[1:2] == 'B':
        return initial_value * 2 + 1

def in_list(name, artist):
    for track in tracks:
        if track.name == name and track.artist == artist:
            return True
    return False


# writes an array to binary file
def write(arr):
    with open('tracks.data', 'wb') as file_handle:
        # store the data as binary data stream
        pickle.dump(arr, file_handle)


# reads from binary file into an array
def read():
    try:
        with open('tracks.data', 'rb') as file_handle:
            # read the data as binary data stream
            read_list = pickle.load(file_handle)
        return read_list
    except:
        print('nothing to read')
        return []


# read data from the binary file
tracks = read()
# choose to read from exported spotify file or not
choice = input('read new data from exportify excel file? (Y/N): ')
if choice == 'y' or choice == 'Y':
    # create pandas DataFrame object from the excel file
    df = pd.read_excel('file:C:/Firefox Downloads/all1.2.xlsx')
    print('Reading from excel...')
    for i, row in df.iterrows():
        if not in_list(row['Track Name'], row['Artist Name']):
            # attempt to get key from older versions
            tried_camelot = try_for_camelot(row['Track Name'], row['Artist Name'])
            genre = get_genre(str(row['Artist Genres']))
            # create new track with metadata from the DataFrame and add to list of tracks
            new_track = Track(row['Track Name'], row['Artist Name'], tried_camelot, int(round(row['Tempo'])), genre)
            tracks.append(new_track)
    print('successfully read')
    # sort by key
    tracks.sort(key=lambda x: x.camelot)
    # write new data to binary file
    write(tracks)

choice = input('Update keys? (Y/N): ')
if choice == 'y' or choice == 'Y':
    i = 0
    for track in tracks:
        if track.camelot == 'N/A':
            print(i, track.name, track.artist)
            new_key = input('New key: ').upper()
            if new_key not in camelots:
                break
            track.camelot = new_key
        i += 1
    # sort by key
    tracks.sort(key=lambda x: x.camelot)
    choice = input('Update persistent file with changes? (Y/N): ')
    if choice == 'y' or choice == 'Y':
        write(tracks)

# decide to write data to local file used during mixing
choice = input('write data to local excel file? (Y/N): ')
if choice == 'y' or choice == 'Y':

    # create 2d array and append metata to each row
    tracks_df = []
    for track in tracks:
        tracks_df.append([track.name, track.artist, track.camelot, track.tempo, track.genre])

    # write data to a new DataFrame object and transfer to excel file
    excel_df = pd.DataFrame(tracks_df, columns={'Track Name', 'Artist Name', 'Key', 'Tempo', 'Genre'})
    excel_df.to_excel(local_excel_file)
    print('Succesfully wrote to', local_excel_file)



