
import requests
import json

buf = json.load(open("secret", 'r'))
UID = buf['UID']
SECRET = buf['SECRET']

HEADERS  = {"Accept": "application/json",    "Content-Type": "application/json",    "Authorization": "Bearer " + SECRET}

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
        # stats
        self.collaborative = data['collaborative']
        self.followers = data['followers']['total']
        # content
        self.tracks = data['tracks']['items']
    
    def __str__(self):
        """Return string representation of playlist"""
        return f"{self.name} ({self.followers} followers)"
    
    def add_track(self, link: str = None, song: "Song" = None):
        """Add a track to the playlist"""
        # append items to playlist
        if link:
            add_song_to_playlist(link, self.link)
        elif song:
            add_song_to_playlist(song.link, self.link, uri = song.uri)

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
        return f"{aspect}={value}&"

    def generate_config_string(self):
        """Generate search configuration string"""
        return f"{self.ENDPOINT}" + "".join([self.get_config_aspect_str(aspect, value) for aspect, value in self.args.items() if value != '_'])
    
    def get_recommendations(self):
        """Get recommendations from spotify"""
        if self._collected: return self.recommendations
        self._collected = True
        res = requests.get(self.generate_config_string(), headers=HEADERS)
        # parse
        self.recommendations = []
        result = res.json()
        tracks = result['tracks']
        for track in tracks:
            print(track['external_urls']['spotify'])
            self.recommendations.append(Song(track['external_urls']['spotify']))
        return self.get_recommendations()

# ------------------------------- #
# functions

def get_playlist_data_raw(link: str) -> dict:
    """Returns the data of the given playlist."""
    ll = "https://api.spotify.com/v1/playlists/"
    if len(link.split('?')) > 1:
        ll += link.split('?')[0].split('/')[-1]
    else: ll = link
    res = requests.get(ll, headers=HEADERS)
    return res.json()

def get_song_data_raw(link: str) -> dict:
    """Returns the data of the given song."""
    ll = "https://api.spotify.com/v1/tracks/"
    if len(link.split('?')) > 1:
        ll += link.split('?')[0].split('/')[-1]
    res = requests.get(ll, headers=HEADERS)
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
    r = requests.post(route, data=json.dumps(data), headers=HEADERS)
    pid = r.json()['id']
    return Playlist("https://api.spotify.com/v1/playlists/" + pid)

def add_song_to_playlist(song_link: str, playlist_link: str, uri: str = None):
    """Add a song to the given playlist."""
    # get song uri
    song_uri = get_song_data_raw(song_link)['uri'] if not uri else uri
    # get playlist id
    playlist_id = playlist_link.split('/')[-1]
    # post data to spotify url
    data = {
        "uris": [song_uri]
    }
    r = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", data=json.dumps(data), headers=HEADERS)
    return r.json()


# ------------------------------- #
# main

# playlist = create_playlist("sample1", "sample for generating playlists")
playlist = Playlist("https://open.spotify.com/playlist/7eMqBWauas5mg8wKkHgldg?si=16ebdfa6e29243a8")

# endpoint
endpoint = "https://api.spotify.com/v1/recommendations?"

seed_song = Song('https://open.spotify.com/track/45HHTHXv7gQ5q2r89ui2Fy?si=28c6f22236904025')

rec = Recommendation(limit=10, market="US", seed_tracks=seed_song.get_song_uri_id(), target_danceability=0.8)
rec.get_recommendations()

for r in rec.get_recommendations():
    print(r)

# # parameters
# limit = 10
# market = "US"
# seed_genres = "indie"
# seed_tracks = seed_song.get_song_uri_id()
# target_danceability = 0.8

# print(seed_song.get_song_uri_id())

# query = f'{endpoint}limit={limit}&market={market}&seed_tracks={seed_tracks}&target_danceability={target_danceability}'
# response = requests.get(query, headers=HEADERS)

# # output
# json_response = response.json()

# uris = []
# for i in json_response['tracks']:
#     uris.append(i)
#     print(i)
#     print(f"\"{i['name']}\" by {i['artists'][0]['name']}")
