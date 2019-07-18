"""
Reads a `.txt` file of newline or '|' delimited URLs,
to batch-download video files, using `youtube-dl`.
"""

from multiprocessing import Pool
from os import system as sys

def opn_list(file):
    with open(file) as f:
        f = f.read()
        if '|' in f:
            vids_list = f.split('|')
        else:
            vids_list = f.split('\n')
    return vids_list

def ytdl(url):
	sys(f'youtube-dl {url}')


vids_list = opn_list("files.txt")

pool = Pool(processes=16)

pool.map(ytdl, vids_list)