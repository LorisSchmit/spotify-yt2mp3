#spotify-yt2mp3: The script that downloads your Spotify library as mp3 from youtube videos

This script allows you to automatically make a local backup of your Spotify library. If the script is run it detects changes (eg. songs added to a playlist) and downloads them as a mp3 file from the most appropriate youtube video. Every mp3 file is tagged with the ID3 tags and the album cover is added. The songs are then organized in folders according to their playlist/album. 

## Usage
###Download specific album or playlist:

<pre>
python3 manage.py <i>type name</i>
</pre>

Type being either playlist or album and name the of playlist/album

###Update specific album or playlist:
<pre>
python3 update.py <i>name</i>
</pre>

###Update entire downloaded library
<pre>
python3 updateLibrary.py <i>name</i>
</pre>