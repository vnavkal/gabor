"""Functions to obtain videos and convert them to frames and back"""


import glob
import os
import subprocess
import numpy as np
from pytube import YouTube


VIDEO_ID = '5v35T_XPGgw'


def download_video(filename):
    yt = YouTube('https://www.youtube.com/watch?v={0}'.format(VIDEO_ID))
    video = yt.get('mp4', '720p')
    video.download(filename)
    return video


def capture_frames(filename, frequency, num_frames):
    for i, time in enumerate(np.linspace(0, num_frames / frequency, num_frames)):
        subprocess.call([
            'ffmpeg',
            '-i',
            filename,
            '-vcodec',
            'png',
            '-ss',
            str(time.round(3)),
            '-vframes',
            '1',
            '-an',
            '-f',
            'rawvideo',
            os.path.join('frames', 'frame{0}.png'.format(str(i).zfill(5)))
        ])


def assemble_frames(output_filename, input_directory, frequency):
    subprocess.call([
        'ffmpeg',
        '-f',
        'image2',
        '-r',
        str(frequency),
        '-i',
        os.path.join(input_directory, 'frame%05d.png'),
        '-vcodec',
        'mpeg4',
        '-y',
        output_filename
    ])
