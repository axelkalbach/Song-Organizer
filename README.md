# Music Organizer
This script allows spotify playlists to be added to a local list of tracks and an excel sheet to be created with metadata from the tracks. It also allows for the user to find songs in the same key, relative major/minor, or a pitched up or down key by one whole tone.
# Installation
1. Clone this repository
```
git clone https://github.com/axelkalbach/Song-Organizer
```
2. Ensure [python](https://www.python.org/downloads/) is installed
3. Install requirements
```
pip install -r requirements.txt
```
# Usage
### Add New Songs
1. Use [this exportify tool](https://watsonbox.github.io/exportify/) to download one of your spotify playlists (make sure to enable include audio features data in settings)
2. Click the 'Add Songs' button and select your .csv exportify file
3. Your songs will be added to a local file
### Export to Excel
1. Ensure you have created a .xlsx workbook
2. Click the 'Export to Excel File' button and select your workbook
3. The workbook will be updated with your songs and metadata
### Find Songs in Similar Key
1. Choose the key of your song in the dropdown menu
2. Click the 
