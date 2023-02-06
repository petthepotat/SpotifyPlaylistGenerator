
import subprocess
import requests
import json
import base64

buf = json.load(open("secret", 'r'))
PRELOAD_BUF = buf

# important data
UID = buf['UID']
CID = buf['CLIENTID']
CSECRET = buf["CLIENTSECRET"]
REFRESHTOKEN = buf['REFRESHTOKEN']
ACCESSTOKEN = buf['ACCESSTOKEN']

# constants
SCOPE = "playlist-modify-private,playlist-modify-public,playlist-read-private,playlist-read-collaborative,user-read-email"
HEADERS  = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESSTOKEN
}
REDIRECT = "https://localhost"


# ------------------------------- #
# classes

class Playlist:
    def __init__(self, link: str):
        """Load data from given spotify link"""
        data = get_playlist_data_raw(link)
        
        # playlist general
        self.name = data['name']
        self.description = data['description']
        self.link = data['external_urls']['spotify']
        self.id = data['id']
        # stats
        self.collaborative = data['collaborative']
        self.followers = data['followers']['total']
        # content
        self.tracks = data['tracks']['items']
    
    def __str__(self):
        """Return string representation of playlist"""
        return f"{self.name} ({self.followers} followers)"
    
    def add_songs(self, songs: list):
        """Add songs to playlist"""
        # print([x.uri for x in songs])
        base = f"https://api.spotify.com/v1/playlists/{self.id}/tracks?uris={'%2C'.join([x.uri.replace(':', '%3A') for x in songs])}"
        res = requests.post(base, headers=HEADERS)
        if res.status_code != 200:
            refresh_token_validity()
            res = requests.post(base, headers=HEADERS)
        return res.json()

class Song:
    def __init__(self, link: str):
        """Get data about song"""
        data = get_song_data_raw(link)

        # song general
        self.name = data['name']
        self.link = data['external_urls']['spotify']
        self.uri = data['uri']
        # artists
        self.artists = data['artists']
        self.artist_names = [artist['name'] for artist in self.artists]
        # album
        self.album = data['album']['name']
        self.album_link = data['album']['external_urls']['spotify']
        self.album_cover = data['album']['images'][0]['url']
        # stats
        self.popularity = data['popularity']
        self.duration = data['duration_ms']
        self.explicit = data['explicit']
    
    def get_song_uri_id(self):
        """Return the uri id of the song"""
        return self.uri.split(':')[-1]

    def __str__(self):
        """Return string representation of song"""
        return f"{self.name} by {', '.join(self.artist_names)}"

class Recommendation:
    ENDPOINT = "https://api.spotify.com/v1/recommendations?"
    def __init__(self, limit: int = 10, market: str = "US", seed_artists: str = "_", 
                seed_genres: str = "_", seed_tracks: str = "_", min_acousticness: float = "_", 
                max_acousticness: float = "_", min_danceability: float = "_", min_duration_ms: int = "_",
                **kwargs):
        # private
        self._collected = False
        self.args = {
            "limit": limit,
            "market": market,
            "seed_artists": seed_artists,
            "seed_genres": seed_genres,
            "seed_tracks": seed_tracks,
            "min_acousticness": min_acousticness,
            "max_acousticness": max_acousticness,
            "min_danceability": min_danceability,
            "min_duration_ms": min_duration_ms,
        }
        for a, v in kwargs.items():
            self.args[a] = v

        # public
        self.recommendations = []

    def get_config_aspect_str(self, aspect: str, value: str):
        """Return the aspect string"""
        return f"{aspect}={value}"

    def generate_config_string(self):
        """Generate search configuration string"""
        return f"{self.ENDPOINT}" + "&".join([self.get_config_aspect_str(aspect, value) for aspect, value in self.args.items() if value != '_'])
    
    def get_recommendations(self):
        """Get recommendations from spotify"""
        if self._collected: return self.recommendations
        self._collected = True
        # get data
        res = requests.get(self.generate_config_string(), headers=HEADERS)
        if res.status_code != 200:
            refresh_token_validity()
            res = requests.get(ll, headers=HEADERS)
        # parse)
        self.recommendations = []
        result = res.json()
        tracks = result['tracks']
        for track in tracks:
            # print(track["href"])
            self.recommendations.append(Song(track["href"]))
        return self.get_recommendations()

# ------------------------------- #
# functions

def refresh_token_validity():
    """Checks if the token is valid."""
    global HEADERS
    print("Refreshing TOKEN")
    url = 'https://accounts.spotify.com/api/token'
    message = f"{CID}:{CSECRET}"
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESHTOKEN,
    }
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {base64_message}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    res = requests.post(url, data=data, headers=headers)
    # print(res.json())
    # save data in file
    new_data = {
        "UID": UID,

        "CLIENTID": CID,
        "CLIENTSECRET": CSECRET,

        # "REFRESHTOKEN": res.json()['refresh_token'],
        "REFRESHTOKEN": REFRESHTOKEN,
        "ACCESSTOKEN": res.json()['access_token']
    }
    # reset variables
    global ACCESSTOKEN
    ACCESSTOKEN = new_data['ACCESSTOKEN']
    with open("secret", 'w') as f:
        json.dump(new_data, f, indent=4)
    HEADERS["Authorization"] = f"Bearer {ACCESSTOKEN}"
    print("Token Refreshed")

def get_playlist_data_raw(link: str) -> dict:
    """Returns the data of the given playlist."""
    ll = "https://api.spotify.com/v1/playlists/"
    if len(link.split('?')) > 1:
        ll += link.split('?')[0].split('/')[-1]
    else: ll = link
    res = requests.get(ll, headers=HEADERS)
    if res.status_code != 200:
        refresh_token_validity()
        res = requests.get(ll, headers=HEADERS)
    return res.json()

def get_song_data_raw(link: str) -> dict:
    """Returns the data of the given song."""
    ll = "https://api.spotify.com/v1/tracks/"
    if len(link.split('?')) > 1:
        ll += link.split('?')[0].split('/')[-1]
    else: ll = link
    # have the track link
    # print(ll)
    res = requests.get(ll, headers=HEADERS)
    if res.status_code != 200:
        refresh_token_validity()
        res = requests.get(ll, headers=HEADERS)
    # got the data
    return res.json()

def create_playlist(name: str, des: str, public: bool = True):
    """Creates a playlist with the given name."""
    route = f"https://api.spotify.com/v1/users/{UID}/playlists"
    # post data to spotify url
    data = {
        "name": name,
        "description": des,
        "public": public
    }
    handle_token_validity()
    res = requests.post(route, data=json.dumps(data), headers=HEADERS)
    if res.status_code != 200:
        refresh_token_validity()
        res = requests.get(ll, headers=HEADERS)
    pid = res.json()['id']
    return Playlist("https://api.spotify.com/v1/playlists/" + pid)

# ------------------------------- #
# main

# playlist = create_playlist("sample1", "sample for generating playlists")
playlist = Playlist("https://open.spotify.com/playlist/7eMqBWauas5mg8wKkHgldg?si=52070a388cba451c")
endpoint = "https://api.spotify.com/v1/recommendations?"
seed_song = Song('https://open.spotify.com/track/45HHTHXv7gQ5q2r89ui2Fy?si=28c6f22236904025')

rec = Recommendation(limit=10, market="US", seed_tracks=seed_song.get_song_uri_id(), target_danceability=0.8)
rec.get_recommendations()
playlist.add_songs(rec.get_recommendations())



