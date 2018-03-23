import cv2
import numpy as np
import os

def extract_frames(file):
    cap = cv2.VideoCapture(file)

    try:
        if not os.path.exists('photos'):
            os.makedirs('photos')
    except OSError:
        print("Error: Creating directory of 'photos'.")

    currentFrame = 0

    for i in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):

        ret, frame = cap.read()

        name = "./photos/" + os.path.splitext(file)[0] + '_' + str(currentFrame) + ".jpg"
        
        print("creating......   " + name)
        
        cv2.imwrite(name, frame)

        currentFrame += 1

files = [f for f in os.listdir('.') if os.path.isfile(f) and "extract_frames.py" not in f]

for file in files:
    extract_frames(file)