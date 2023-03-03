from scripts import spotifyapi, runnode, utils
import os

# while loop for user input + downloading songs

if not os.path.exists("assets"):
    os.mkdir("assets")

while True:
    link = input("Input a playlist link: ")
    if not link:
        break
    playlist = spotifyapi.Playlist(link)

    # download songs
    paths = runnode.download_songs(
        songs=playlist.get_songs(),
        path="assets/" + utils.remove_illegal_file_chars(playlist.name),
    )
    # done
    print("Done downloading songs!")
    print("--" * 20)
