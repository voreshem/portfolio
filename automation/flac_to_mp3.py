### Converts folder of FLAC audio files to subfolder of MP3 files, using ffmpeg ###

import os
import glob
from multiprocessing import Pool

def to_mp3(file):
    os.system(f"~/ffmpeg_sources/ffmpeg/ffmpeg -i '{file}' -acodec libmp3lame -ab 320k 'mp3s/{file.replace('flac','mp3')}'")

if __name__ == "__main__":
    song_list = glob.glob("*.flac")

    try:
        if not os.path.exists('mp3s'):
            os.makedirs('mp3s')
    except OSError:
        print("Error: Creating dir of 'mp3s'.")

    pool = Pool(processes=(int(os.cpu_count())))
    pool.map(to_mp3, song_list)

print("\n\nDONE!\n")