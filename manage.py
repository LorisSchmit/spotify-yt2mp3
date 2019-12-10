from fetchPlaylist import getAlbum, getPlaylist
from download import *
import eyed3
import urllib.error
import os
from pathlib import Path

def get(what,name):
    found = False

    if what == "album":
        songs = getAlbum(name)
        found = True
    elif what == "playlist":
        songs = getPlaylist(name)
        found = True
    else:
        print("Incorrect Type")

    if found and len(songs)>0:
        dirpath = str(Path.home())+"/Spotify"

        try:
            # Create target Directory
            os.mkdir(dirpath)
            print("Directory Spotify created ")
        except FileExistsError:
            pass

        try:
            # Create target Directory
            os.mkdir(dirpath+"/"+name)
            print("Directory ", name , " created ")
        except FileExistsError:
            pass

        path = dirpath+"/"+name

        counter = 0
        for song in songs:
            try:
                download(youtube_query(song.title + " " +song.artist + " lyrics"), path, song.title)
            except youtube_dl.utils.ExtractorError:
                pass
            counter += 1
            file_path = path + "/" + song.title+".mp3"
            audiofile = eyed3.load(file_path)
            audiofile.tag.artist = song.artist
            audiofile.tag.title = song.title
            audiofile.tag.album = song.album
            audiofile.tag.track_num = counter
            try:
                response = urlopen(song.image_url)
                imagedata = response.read()
                audiofile.tag.images.set(3, imagedata, "image/jpeg", u"")
            except urllib.error.HTTPError as e:
                print(e)
            audiofile.tag.save()
    else:
        print(name+ " not found")

if __name__ == "__main__":
    what = str(sys.argv[1])
    name = str(sys.argv[2])
    get(what,name)




