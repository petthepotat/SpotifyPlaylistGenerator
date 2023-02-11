from scripts import spotifyapi, runnode

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
2. IMPROATJPAOJ PWAJ 
- MULTIPLE seed songs!!!!!
3. 

long term
1. allow different users to get playlists generated for them
"""


seed_song = spotifyapi.Song(
    "https://open.spotify.com/track/3BDcHGw6wUIisZJw0ndKQb?si=f35d00c330434d90"
)
# seed_song = spotifyapi.Song(input("Input a seed song link: "))
songs = [seed_song]
# for i in range(int(input("How many more seed songs?: "))):
# songs.append(spotifyapi.Song(input(f"Input a {i+1} link: ")))

# exit()

# playlist = spotifyapi.create_playlist("insert name", "generated by petthepotat SpotifyGenerator :)")
# playlist = spotifyapi.Playlist(
#     "https://open.spotify.com/playlist/0EolJ8nv19zQXm9Va1W0YH?si=a740408c32f14df5"
# )
# playlist.add_songs(songs=[seed_song])
rec = spotifyapi.Recommendation(
    limit=5,
    market="US",
    seed_tracks=spotifyapi.Recommendation.generate_seed_song_array(songs),
    danceability=seed_song.danceability,
    energy=seed_song.energy,
    instrumentalness=seed_song.instrumentalness,
    liveness=seed_song.liveness,
    loudness=seed_song.loudness,
    speechiness=seed_song.speechiness,
    tempo=seed_song.tempo,
    valence=seed_song.valence,
)
runnode.download_songs(rec.get_recommendations())
# playlist.add_songs(rec.get_recommendations())
