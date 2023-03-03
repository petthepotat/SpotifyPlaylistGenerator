import subprocess
from . import youtubehandler

import os
from typing import List


# ------------------------------- #
# function


def download_songs(songs: List[str], path: str = "assets"):
    """Download songs from youtube"""
    # check if path exists
    if not os.path.exists(path):
        os.mkdir(path)

    # Read the Node.js script
    node_script = open("scripts/runnode.js", "r").read()
    # get links for videos -- to collect songs
    print("Collecting Data From Youtube")
    custom_vars = [path] + [youtubehandler.search(name) for name in songs]

    print(custom_vars)
    print("Start downloading")
    command = ["node", "-e", node_script] + custom_vars
    
    # cal a process to run the node script and pipe console output to seprate thread
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # read the output
    processes = {}
    finished = 0
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            # collect data
            line = output.strip().decode("utf-8").split('|')
            if line[0] == "START":
                processes[line[1]] = "0%"
            elif line[0] == "UPDATE":
                processes[line[1]] = line[2]
            elif line[0] == "FINISHED":
                processes[line[1]] = "100%"
                finished += 1
        # print the progress
        os.system("cls")
        # output necassary data
        print(f"Path: {path} | Songs: {len(songs)} | Downloaded: {finished}")
        # output song download data
        for key, value in processes.items():
            print(f"{key:16}: {value:5}")
        
        
    # get the return code
    rc = process.poll()

    # output errors
    for line in process.stderr.readlines():
        print(line.decode("utf-8"), end='')
    
    # generate a list of paths to downloaded files
    return [os.path.join(path, x.split("|")[0] + ".mp3") for x in custom_vars]


def save_paths_to_file(paths: List[str], file_path: str):
    """Save a list of paths to a file"""
    with open(file_path, "w") as f:
        f.write("\n".join(paths))
