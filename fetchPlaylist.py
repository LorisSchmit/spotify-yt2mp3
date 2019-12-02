import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import requests
import json
from Song import Song

def getJSON(access_token,what):
    PLAYLIST_URL = "https://api.spotify.com/v1/me/"+what

    PARAMS = {
        'access_token': access_token
    }
    r = requests.get(PLAYLIST_URL, params=PARAMS)
    data = r.json()
    items = data['items']
    pl_list = []
    for item in items:
        if what == "playlists":
            pl_list.append([item['id'], item['name']])
        elif what == "albums":
            pl_list.append([item['album']['id'], item['album']['name']])
    return pl_list


def getToken():
    AUTH_URL = "https://accounts.spotify.com/api/token"
    with open("spotify_tokens",mode="r") as file:
        refresh_token = file.readline()
        client_id = file.readline()
        client_secret = file.readline()
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    data = {
        'refresh_token': refresh_token,
        'redirect_uri': 'http://localhost:8888',
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret
    }
    p = requests.post(AUTH_URL, headers=headers, data=data)
    auth_data = p.json()
    access_token = auth_data['access_token']

    return access_token

def getPlaylist(to_download):
    try:
        with open("token") as f:
            access_token = f.readline()
        f.close()
        pl_list = getJSON(access_token,'playlists')
        print("token from file")
    except KeyError:
        access_token = getToken()
        f = open("token","w")
        f.write(access_token)
        f.close()
        print("new token")
        pl_list = getJSON(access_token,'playlists')
    songs = []
    for pl in pl_list:
        if pl[1] == to_download:
            URL = "https://api.spotify.com/v1/playlists/"+pl[0]+"/tracks"

            PARAMS = {
                'access_token': access_token
            }
            r = requests.get(URL, params=PARAMS)
            data = r.json()
            #print(json.dumps(data, indent=4, sort_keys=True))
            items = data['items']
            items2 = []
            if data['total'] > 100:
                PARAMS2 = {
                    'access_token': access_token,
                    'offset': 100
                }
                r2 = requests.get(URL, params=PARAMS2)
                data2 = r2.json()
                items2 = data2['items']

            for item in items:
                title = item['track']['name'].replace("/","-")
                artist = item['track']['artists'][0]['name']
                album = item['track']['album']['name']
                date_added = item['added_at']
                image_url = item['track']['album']['images'][0]['url']
                song = Song(title,artist,album,date_added,image_url)
                songs.append(song)
            for item in items2:
                title = item['track']['name'].replace("/", "-")
                artist = item['track']['artists'][0]['name']
                album = item['track']['album']['name']
                date_added = item['added_at']
                image_url = item['track']['album']['images'][0]['url']
                song = Song(title, artist, album, date_added, image_url)
                songs.append(song)
    return songs

def getAlbum(to_download):
    try:
        with open("token") as f:
            access_token = f.readline()
        f.close()
        pl_list = getJSON(access_token, 'albums')
        print("token from file")
    except KeyError:
        access_token = getToken()
        f = open("token","w")
        f.write(access_token)
        f.close()
        print("new token")
        pl_list = getJSON(access_token, 'albums')
    songs = []
    for pl in pl_list:
        if pl[1] == to_download:

            URL = "https://api.spotify.com/v1/me/albums"

            ALBUM_URL = "https://api.spotify.com/v1/albums/"+pl[0]+"/tracks"

            PARAMS = {
                'access_token': access_token
            }
            r = requests.get(URL, params=PARAMS)
            data = r.json()
            albums = data['items']

            for album in albums:
                if album['album']['name'] == to_download:
                    date_added = album['added_at']
                    image_url = album['album']['images'][0]['url']

            r_album = requests.get(ALBUM_URL, params=PARAMS)
            data_album = r_album.json()
            items = data_album['items']
            for item in items:
                title = item['name']
                artist = item['artists'][0]['name']
                album = to_download
                song = Song(title,artist,album,date_added,image_url)
                songs.append(song)
    return songs