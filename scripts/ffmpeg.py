import subprocess
import sys

from typing import List
import PIL


"""


ffmpeg -i input1.mp3 -t 15 -i input2.mp3 -t 15 -filter_complex "[0:0][1:0]concat=n=2:v=0:a=1[out]" -map "[out]" output.mp3


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


class FFmpegImageVideoGenerator:
    @classmethod
    def make_pair(cls, command: str, value: str):
        """Make a pair of a command and a value"""
        return f"{command} {value}"

    # ------------------------------- #

    def __init__(self, image_file: str, input_files: List[str]):
        """
        FFmpeg handler
        given:
        - input image (the background of the entire video)
        - file (contains all the audio tracks to be joined together)
        - duration (the duration of the video)
        - output file (the output file)
        """
        self.target_file = target
        # args
        self.input_file = self.make_pair(TARGET_IMG, value)
        self.video_codec = ""

    def run_process(self):
        """Run the ffmpeg process"""
        # build the command
        command = [FFMPEGPATH]
        # add the options
        for key, value in self.options.items():
            command.append(key)
            command.append(value)
        # add the target
        command.append(self.target)

        # run the process
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        # read output
        output, error = process.communicate()
        print(output.decode().strip())
        print(error)


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
