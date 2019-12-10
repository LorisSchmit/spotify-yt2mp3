from fetchPlaylist import getPlaylists
import manage
import update
import os
from pathlib import Path

def downloadLibrary():
	playlists = getPlaylists()
	path = str(Path.home())+"/Spotify"
	try:
		# Create target Directory
		os.mkdir(path)
		print("Directory Spotify created ")
	except FileExistsError:
		pass
	already_downloaded = os.listdir(path)

	for playlist in playlists:
		if not (playlist[1] in already_downloaded):
			print("Downloading "+playlist[1])
			manage.get("playlist",playlist[1])

def updateLibrary():
	playlist = getPlaylists()
	for playlist in playlists:
		update.update(playlist[1])

if __name__ == "__main__":
	downloadLibrary()