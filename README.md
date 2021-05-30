# Music Organizer
This script allows spotify playlists to be added to a local list of tracks and an excel sheet to be created with metadata from the tracks. It also allows for the user to find songs in the same key, relative major/minor, or a pitched up or down key by one whole tone.
# Installation
1. Clone this repository: ```git clone https://github.com/axelkalbach/Song-Organizer```
2. Ensure [python](https://www.python.org/downloads/) is installed
3. Install requirements: ```pip install -r requirements.txt```
# Usage
### Running the Program
1. Navigate to your directory in the command line: ```cd /Your-Directory```
2. Run the python script with your spotify username: ```python music_organizer.py [your username]```
### Adding New Songs
1. Click 'Update Songs'
2. All tracks from your public playlists will be added
3. When quitting, you will be asked if you want to save the changes with the new added tracks
### Exporting to Excel
1. Ensure you have created a .xlsx workbook
2. Click the 'Export to Excel File' button and select your workbook
3. The workbook will be updated with your songs and metadata
### Finding Songs in Similar Key
1. Choose the key of your song in the dropdown menu
2. Click the 'Find Songs' Button and a new window will appear
3. Listed will be songs in the same key, the relative major or minor, and songs that are pitched 1 whole tone up or down
