'''
Takes an image,
compresses to a given size in KB,
preserves its original resolution,
then generates images which analyze differences.
'''

import os
import argparse

class Image(object):
    def __init__(self, args):
        self.input = args.img
        self.dir = os.path.dirname(self.input)
        self.name = os.path.basename(self.input)
        self.no_ext = os.path.splitext(self.name)[0]
        self.path = os.path.abspath(self.input)
        self.comp_dir = f"{self.dir}/{self.no_ext}"
        self.comp_path = f"{self.comp_dir}_comp_{args.file_size}.jpg"
        self.comp_name = os.path.basename(self.comp_path)
        self.comp_dest = f"{self.comp_dir}/{self.comp_name}"
        self.diff = f"{self.comp_dir}/{self.no_ext}_comp_difference.png"


def convert(image, file_size):
    print(f"\n\nConverting {image.name} to {file_size}KB...")
    sh = f"convert {image.path} -define jpeg:extent={file_size}kb {image.comp_path}"
    os.system(sh)

def compare(image):
    print(f"\n\nComparing {image.comp_name} to {image.name}")
    sh = f"compare {image.path} {image.comp_dest} {image.diff}"
    os.system(sh)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store',dest='img', help='full path to an image')
    parser.add_argument('-s', action='store', dest='file_size')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    image = Image(args)
    file_size = args.file_size
    
    print(f"\n\n{image.name} successfully imported!")

    os.mkdir(image.comp_dir)

    convert(image, file_size)

    os.rename(image.comp_path, image.comp_dest)
    
    print(f"\n\n{image.name} successfully converted!")

    compare(image)

    print(f"\n\n{image.name} successfully compared!")

    print("\n\nDONE!\n\n")

if __name__ == '__main__':
    main()
