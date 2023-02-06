
from scripts import spotifyapi

# ------------------------------- #
# main

playlist = spotifyapi.create_playlist("sample2", "sample for generating playlists")
# playlist = spotifyapi.Playlist("https://open.spotify.com/playlist/7eMqBWauas5mg8wKkHgldg?si=52070a388cba451c")

endpoint = "https://api.spotify.com/v1/recommendations?"
seed_song = spotifyapi.Song('https://open.spotify.com/track/45HHTHXv7gQ5q2r89ui2Fy?si=28c6f22236904025')

print(seed_song)

exit()

rec = spotifyapi.Recommendation(
        limit=20, market="US", seed_tracks=seed_song.get_song_uri_id(), 
        target_danceability=0.6, min_acousticness=0.5)
rec.get_recommendations()
playlist.add_songs(rec.get_recommendations())



