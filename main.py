
from scripts import spotifyapi

# ------------------------------- #
# main

# playlist = spotifyapi.create_playlist("sample2", "sample for generating playlists")
# # playlist = spotifyapi.Playlist("https://open.spotify.com/playlist/7eMqBWauas5mg8wKkHgldg?si=52070a388cba451c")

# endpoint = "https://api.spotify.com/v1/recommendations?"
# seed_song = spotifyapi.Song('https://open.spotify.com/track/45HHTHXv7gQ5q2r89ui2Fy?si=28c6f22236904025')

# print(seed_song)
"""
TODO: 
short term
1. function for generating playlists -- or make a class lmao

long term
1. allow different users to get playlists generated for them
"""


playlist = spotifyapi.create_playlist("andrew test", "sus not sus")
seed_song = spotifyapi.Song("https://open.spotify.com/track/7rhPtZ2nmgkrv6MCCDF2WU?si=8388fa369e324f84")

# exit()

playlist.add_songs(songs=[seed_song])
rec = spotifyapi.Recommendation(
        limit=20, market="US", seed_tracks=seed_song.get_song_uri_id(),
        danceability=seed_song.danceability, energy=seed_song.energy,
        instrumentalness=seed_song.instrumentalness, liveness=seed_song.liveness,
        loudness=seed_song.loudness, speechiness=seed_song.speechiness,
        tempo=seed_song.tempo, valence=seed_song.valence
)
rec.get_recommendations()
playlist.add_songs(rec.get_recommendations())



