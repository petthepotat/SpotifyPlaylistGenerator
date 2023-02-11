import subprocess
from . import youtubehandler

from typing import List


# ------------------------------- #
# function


def download_songs(songs: List[str]):
    """Download songs from youtube"""
    # Read the Node.js script
    node_script = open("scripts/runnode.js", "r").read()
    # get links for videos -- to collect songs
    custom_vars = [youtubehandler.search(name) for name in songs]
    # print(custom_vars)
    command = ["node", "-e", node_script] + custom_vars
    # Create a Node.js process
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    # Read the output of the Node.js process
    output, error = process.communicate()
    # Print the output of the Node.js process
    print(output.decode().strip())
    print(error) # outputs None

    # generate a list of paths to downloaded files
    return ["assets/" + x.split("|")[0] + ".mp3" for x in custom_vars]


def save_paths_to_file(paths: List[str], file_path: str):
    """Save a list of paths to a file"""
    with open(file_path, "w") as f:
        f.write("\n".join(paths))
