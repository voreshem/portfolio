"""
Converts a folder full of camera MP4 files, using ffmpeg,
to MOV files that DaVinci Resolve, on Fedora Linux, can use.
"""

import os
from os import system as sys
from multiprocessing import Pool

mp4_files = [file[:-4] for file in os.listdir() if file[-3:] == 'mp4']

def convert_mp4(file):
	sys(f"ffmpeg -i {file}.mp4 -vcodec dnxhd -acodec pcm_s16le -s 1920x1080 -r 30000/1001 -b:v 36M -pix_fmt yuv422p -f mov {file}.mov")


pool = Pool(processes=(int(os.cpu_count()/4)))

pool.map(convert_mp4, mp4_files)