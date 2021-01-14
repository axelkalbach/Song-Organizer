import pandas as pd
import pickle
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

key_camelots = ['1A - Ab Minor',
                '1B - B Major',
                '2A - Eb Minor',
                '2B - F# Major',
                '3A - Bb Minor',
                '3B - Db Major',
                '4A - F Minor',
                '4B - Ab Major',
                '5A - C Minor',
                '5B - Eb Major',
                '6A - G Minor',
                '6B - Bb Major',
                '7A - D Minor',
                '7B - F Major',
                '8A - A Minor',
                '8B - C Major',
                '9A - E Minor',
                '9B - G Major',
                '10A - B Minor',
                '10B - D Major',
                '11A - F# Minor',
                '11B - A Major',
                '12A - Db Minor',
                '12B - E Major']

camelots = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B', '7A', '7B', '8A', '8B', '9A', '9B',
            '10A', '10B', '11A', '11B', '12A', '12B']


# track class used throughout, contains metadata about a given track
class Track:
    def __init__(self, name, artist, camelot, tempo, genre):
        self.name = name
        self.artist = artist
        self.camelot = camelot
        self.tempo = tempo
        self.genre = genre

    def __repr__(self):
        return '{:50.50}{:50.50}{:5}{:<6}\n'.format(self.name, self.artist, self.camelot, self.tempo)


# prints song list in easy to read format
def print_list(song_list):
    fin = ''
    for track in song_list:
        fin += (str(track) + '\n')
    return fin


# swaps letter (A or B) at end of camelot given
def get_relative_major_minor(camelot):
    if camelot[1] == 'A':
        return camelot[0] + 'B'
    else:
        return camelot[0] + 'A'


# finds key that is one tone lower than given
def get_key_down(camelot):
    int_value = (int(camelot[0:1]) + 5) % 12
    if int_value == 0:
        int_value = 12
    return str(int_value) + camelot[1:2]


# finds key that is one tone higher than given
def get_key_up(camelot):
    int_value = (int(camelot[0:1]) + 7) % 12
    if int_value == 0:
        int_value = 12
    return str(int_value) + camelot[1:2]


# gets a simplistic form of the track's genre given the list of genres from the exportify file
def get_genre(input_genre):
    if 'rap' in input_genre.lower():
        return 'Rap'
    if 'edm' in input_genre.lower():
        return 'EDM'
    if 'pop' in input_genre.lower():
        return 'Pop'
    return 'Misc.'


# changes a key value from its alphanumeric value to a numeric one
def get_key_value(input_key):
    initial_value = int(input_key[0:1])
    if input_key[1:2] == 'A':
        return initial_value * 2
    if input_key[1:2] == 'B':
        return initial_value * 2 + 1


# checks if a given track exists in the local tracks file
def in_list(name, artist):
    for track in tracks:
        if track.name == name and track.artist == artist:
            return True
    return False


# converts the format of (key value, mode) form exportify file to camelot for local use
def get_camelot(key_value, mode):
    ordered_camelots = [['5A', '12A', '7A', '2A', '9A', '4A', '11A', '6A', '1A', '8A', '3A', '10A'],
                        ['8B', '3B', '10B', '5B', '12B', '7B', '2B', '9B', '4B', '11B', '6B', '1B']]
    return ordered_camelots[mode][key_value]


# reads from exportify file and writes to local tracks file
def read_from_exportify(status):
    # query for exportify location
    Tk().withdraw()
    exportify_file = askopenfilename(initialdir=os.getcwd(), title="Select your exportify file")
    # create pandas DataFrame object from the excel file
    df = pd.read_excel(exportify_file)
    print('Reading from excel...')
    status.config(text='Reading from excel...')
    initial_length = len(tracks)
    for i, row in df.iterrows():
        if not in_list(row['Track Name'], row['Artist Name']):
            camelot = get_camelot(row['Key'], row['Mode'])
            genre = get_genre(str(row['Artist Genres']))
            # create new track with metadata from the DataFrame and add to list of tracks
            new_track = Track(row['Track Name'], row['Artist Name'], camelot, int(round(row['Tempo'])), genre)
            tracks.append(new_track)
    new_songs = len(tracks) - initial_length
    print('Successfully added {} songs'.format(new_songs))
    status.config(text='Successfully added {} songs'.format(new_songs))
    # sort by key
    tracks.sort(key=lambda x: x.camelot)
    # write new data to binary file
    write(tracks)
    print('added to local binary file')


# writes song list to excel file
def write_to_excel(status):
    # create 2d array and append metadata to each row
    tracks_df = []
    for track in tracks:
        tracks_df.append([track.name, track.artist, track.camelot, track.tempo, track.genre])

    # write data to a new DataFrame object and transfer to excel file
    excel_df = pd.DataFrame(tracks_df, columns={'Track Name', 'Artist Name', 'Key', 'Tempo', 'Genre'})

    excel_file = askopenfilename(initialdir=os.getcwd(), title="Select Excel file to write to")

    excel_df.to_excel(excel_file)

    status.config(text='Successfully wrote to ' + excel_file)
    print('Successfully wrote to', excel_file)


def find_songs(status, camelot_w_key):
    # create lists for same key, relative major/minor, and key shifts up and down
    same_keys = []
    relative_keys = []
    key_ups = []
    key_downs = []
    camelot = camelots[key_camelots.index(camelot_w_key)]
    relative = get_relative_major_minor(camelot)
    key_up = get_key_up(camelot)
    key_down = get_key_down(camelot)

    # add respective tracks to lists
    for track in tracks:
        if camelot == track.camelot:
            same_keys.append(track)
        elif relative == track.camelot:
            relative_keys.append(track)
        elif key_up == track.camelot:
            key_ups.append(track)
        elif key_down == track.camelot:
            key_downs.append(track)

    same_keys.sort(key=lambda x: x.tempo)
    relative_keys.sort(key=lambda x: x.tempo)
    key_ups.sort(key=lambda x: x.tempo)
    key_downs.sort(key=lambda x: x.tempo)

    status.config(text='Songs found')

    # build new window to display songs found
    song_window = Tk()
    song_window.geometry('800x830')
    song_window.title('Songs Found')

    same_label = Label(song_window, font='Courier 12', text='Same Key')
    same_label.grid(row=0, column=0, sticky=W)
    songs_label_1 = Label(song_window, anchor='w', font='Courier 8',
                          text='{:50}{:50}{:5}{:6}'.format('Track Name', 'Artist', 'Key', 'Tempo'))
    songs_label_1.grid(row=1, column=0, sticky=W)
    same_listbox = Listbox(song_window, width=200, font='Courier 8')
    for i in range(len(same_keys)):
        same_listbox.insert(i, str(same_keys[i]))
    same_listbox.grid(row=2, column=0, sticky=W)

    relative_label = Label(song_window, font='Courier 12', text='Relative Major/Minor')
    relative_label.grid(row=3, column=0, sticky=W)
    songs_label_2 = Label(song_window, anchor='w', font='Courier 8',
                          text='{:50}{:50}{:5}{:6}'.format('Track Name', 'Artist', 'Key', 'Tempo'))
    songs_label_2.grid(row=4, column=0, sticky=W)
    relative_listbox = Listbox(song_window, width=200, font='Courier 8')
    for i in range(len(relative_keys)):
        relative_listbox.insert(i, str(relative_keys[i]))
    relative_listbox.grid(row=5, column=0, sticky=W)

    up_label = Label(song_window, font='Courier 12', text='One Pitch Up (Pitch Down 1 Step to Match Key)')
    up_label.grid(row=6, column=0, sticky=W)
    songs_label_3 = Label(song_window, anchor='w', font='Courier 8',
                          text='{:50}{:50}{:5}{:6}'.format('Track Name', 'Artist', 'Key', 'Tempo'))
    songs_label_3.grid(row=7, column=0, sticky=W)
    up_listbox = Listbox(song_window, width=200, font='Courier 8')
    for i in range(len(key_ups)):
        up_listbox.insert(i, str(key_ups[i]))
    up_listbox.grid(row=8, column=0, sticky=W)

    down_label = Label(song_window, font='Courier 12', text='One Pitch Down (Pitch Up 1 Step to Match Key)')
    down_label.grid(row=9, column=0, sticky=W)
    songs_label_4 = Label(song_window, anchor='w', font='Courier 8',
                          text='{:50}{:50}{:5}{:6}'.format('Track Name', 'Artist', 'Key', 'Tempo'))
    songs_label_4.grid(row=10, column=0, sticky=W)
    up_listbox = Listbox(song_window, width=200, font='Courier 8')
    for i in range(len(key_downs)):
        up_listbox.insert(i, str(key_downs[i]))
    up_listbox.grid(row=11, column=0, sticky=W)

    cancel_btn = Button(song_window, text='Close', command=song_window.destroy)
    cancel_btn.grid(row=12, column=0, sticky=W, padx=5, pady=5)


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


if __name__ == '__main__':

    # read data from the binary file
    tracks = read()

    # build main window
    root = Tk()
    root.title('Song Finder')
    root.geometry('300x200')
    status_var = StringVar()

    f1 = Frame(root)
    f1.pack(pady=5)
    add_btn = Button(f1, text='Add Songs', command=lambda: read_from_exportify(status_label))
    add_btn.pack(side=LEFT, padx=5)
    status_label = Label(root, text='--STATUS--')
    export_btn = Button(f1, text='Export to Excel File', command=lambda: write_to_excel(status_label))
    export_btn.pack(side=LEFT)

    choice = StringVar()
    key_combo = ttk.Combobox(root, values=key_camelots, textvariable=choice, width=15)
    key_combo.current(0)
    key_combo.pack()

    find_btn = Button(root, text='Find Songs', command=lambda: find_songs(status_label, str(choice.get())))
    find_btn.pack(pady=5)

    status_label.pack()

    root.mainloop()



