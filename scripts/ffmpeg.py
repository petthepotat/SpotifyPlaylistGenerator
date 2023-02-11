import subprocess
import sys
import os

import PIL
from PIL import Image, ImageDraw, ImageOps, ImageFilter

from typing import List, Tuple

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
SILENCE = ".blob/silence.mp3"
AUDIOCODEC = "-codec:a libmp3lame"
AUDIOQUALITY = "-qscale:a 2"
CONCATFILE = '-f concat -i ".blob/concat.txt"'

# ------------------------------- #
# functions


def generate_image(
    image_file,
    colors: List[Tuple[int, int, int]],
    target_path: str = "result.jpg",
):
    """Generate an image file"""
    # create a new image
    back = Image.new("RGBA", (1920, 1080), (0, 0, 0))
    # open central image
    c_image = Image.open(image_file).convert("RGBA")
    # draw the background
    draw = ImageDraw.Draw(back)
    # literlaly manual grayscale maths
    for i in range(1080):
        color = (
            int(colors[0][0] + (colors[2][0] - colors[0][0]) * i / 1080),
            int(colors[0][1] + (colors[2][1] - colors[0][1]) * i / 1080),
            int(colors[0][2] + (colors[2][2] - colors[0][2]) * i / 1080),
        )
        draw.line([(0, i), (1920, i)], fill=color)

    # center image on gradient back
    bw, bh = back.size
    iw, ih = c_image.size
    offset = ((bw - iw) // 2, (bh - ih) // 2)
    # add shadow to image
    shadow = ImageOps.colorize(
        # the white = (255, 255, 255, 100) reduces alpha value
        ImageOps.invert(c_image.convert("L")),
        (0, 0, 0, 0),
        (255, 255, 255, 255),
    )
    # resize image ==> then scale to background
    # shadow = shadow.resize((1920, 1920), Image.ANTIALIAS)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=15))
    # steal alpha + reduce alpha
    # r, g, b, ash = shadow.convert("RGBA").split()
    # a = ash.point(lambda x: 100)
    # remerge
    # shadow = Image.merge("RGBA", (r, g, b, ash))

    shadow_offset = (bw - shadow.width) // 2 + 15, (bh - shadow.height) // 2 + 15
    back.paste(shadow, shadow_offset)
    # add image to background
    back.paste(c_image, offset)

    # save the image
    back = back.convert("RGB")
    back.save(target_path)


def generate_mp4(image_file, audio_files, output_file):
    audio_list_file = "audio_list.txt"

    with open(audio_list_file, "w") as f:
        for audio_file in audio_files:
            f.write("file '{}'\n".format(audio_file))
            f.write("file '{}'\n".format(SILENCE))

    if not os.path.exists(SILENCE):
        # create silence.wav
        subprocess.run(
            [
                "ffmpeg",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=48000:cl=stereo",
                "-t",
                "3",
                SILENCE,
            ]
        )

    # concatenate audio files
    cmd = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        audio_list_file,
        "-loop",
        "1",
        "-i",
        image_file,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        output_file,
    ]
    subprocess.run(cmd)

    # remove audio_list_file and silence.wav
    os.remove(audio_list_file)
    # os.remove("silence.wav")


# ------------------------------- #
# testing

generate_image(
    ".blob/image.jpg", [(255, 195, 0), (245, 176, 65), (240, 178, 12)], ".blob/temp.jpg"
)

# generate_mp4(".blob/temp.jpg", ["assets/test.mp3", "assets/test.mp3"], "result.mp4")
