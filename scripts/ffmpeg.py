import subprocess
import sys


"""
ffmpeg options:
    -i: input file
    -c:v: video codec
    -c:a: audio codec
    -b:a: audio bitrate
    -b:v: video bitrate
    -ar: audio sample rate
    
    -ss: start time
    -t: duration
    -to: end time

    -filter:a: audio filter
    -filter:v: video filter

    -pix_fmt: pixel format

    -loop 1: loop the input once

    # joining audio tracks together
    -f concat "filename"

# special option
    concat

    -safe 0: allow unsafe filenames
    -i "filename"
    -c copy: copy the streams
"""

FFMPEGPATH = "ffmpeg"

# video
TARGET_IMG = None
TIMEDURATIONARG = "-t"
LOOPARG = "-loop"
LOOPDEF = "1"
PIXELFORMATARG = "-pix_fmt"
PIXELFORMATDEF = "yuv420p"
VIDEOCODECARG = "-c:v"
VIDEOCODECDEF = "libx264"


# audio
SILENCE = ".blob/silence.wav"
AUDIOCODEC = "-codec:a libmp3lame"
AUDIOQUALITY = "-qscale:a 2"
CONCATFILE = '-f concat -i ".blob/concat.txt"'

# ------------------------------- #
# functions


class FFmpeg:
    def __init__(self, target: str, **kwargs):
        """FFmpeg handler"""
        self.options = {**kwargs}
        # valid kwargs:
        """
        above lmao go check or smth idk
        """
        self.target = target


# ------------------------------- #
# testing


command = [
    FFMPEGPATH,
    LOOPARG,
    LOOPDEF,
    "-i",
    ".blob/image.jpg",
    VIDEOCODECARG,
    VIDEOCODECDEF,
    TIMEDURATIONARG,
    "10",
    PIXELFORMATARG,
    PIXELFORMATDEF,
    "output.mp4",
]

print(command)

process = subprocess.Popen(command, stdout=subprocess.PIPE)
# read output
output, error = process.communicate()
print(output.decode().strip())
print(error)
