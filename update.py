import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import os
import eyed3
from urllib.request import urlopen
import urllib.error
import download
from fetchPlaylist import getPlaylist
from pathlib import Path

if __name__ == "__main__":
    playlist = str(sys.argv[1])

songs = getPlaylist(playlist)

dirpath = str(Path.home())+"/Spotify"

path = dirpath+"/"+playlist

files = os.listdir(path)

new_songs = []

for song in songs:
    found = False
    for file in files:
        song_name = file[:-4]
        if song_name == song.title:
            found = True
    if not found:
        new_songs.append(song)

for song in new_songs:
    print("new song found: "+song.title)
    download.download(download.youtube_query(song.title + " " + song.artist + " lyrics"), path, song.title)
    file_path = path + "/" + song.title + ".mp3"
    audiofile = eyed3.load(file_path)
    audiofile.tag.artist = song.artist
    audiofile.tag.title = song.title
    audiofile.tag.album = song.album
    try:
        response = urlopen(song.image_url)
        imagedata = response.read()
        audiofile.tag.images.set(3, imagedata, "image/jpeg", u"")
    except urllib.error.HTTPError as e:
        print(e)
    audiofile.tag.save()

counter = 0

for song in songs:
    counter += 1
    file_path = path + "/" + song.title + ".mp3"
    audiofile = eyed3.load(file_path)
    audiofile.tag.track_num = counter
    audiofile.tag.save()
