import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
from urllib.parse import urlencode
from urllib.request import urlopen



import re
import youtube_dl
import csv

def youtube_query(query):
        query_string = urlencode({"search_query" : query})
        html_content = urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        url = "http://www.youtube.com/watch?v=" + search_results[0]
        print(url)
        return url

def download(url,path, song_title):
        #s = path+"/"+song_title+".mp3"
        s = path+"/"+song_title+'.%(ext)s'

        ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',}],
                'outtmpl' : s
            }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

