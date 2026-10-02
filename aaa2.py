import sys
import subprocess
import cv2
import numpy as np
import time
import json
import pygame

STEP = 32

scale = np.array(list("$@B%8&WM#ZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.™ "))

width = int(subprocess.check_output(["tput", "cols"]))-1
height = int(subprocess.check_output(["tput", "lines"]))-1
frames=[]
video = cv2.VideoCapture("vid3.mp4")
def makeframes():
    while True:

        success, image = video.read()
        if not success:
            break
        resized = cv2.resize(image, (width - 1, height - 1), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        lum = (0.3126 * rgb[:, :, 0] + 0.4152 * rgb[:, :, 1] + 0.2722 * rgb[:, :, 2])
        ind = (lum / 255.0 * (len(scale) - 1)).astype(int)
        chars = scale[ind]


        output = "\033[H" + "\n".join("".join(row) for row in chars)
        frames.append(output)
makeframes()
with open("data.json", "w") as file:
    json.dump(frames, file)
with open("data.json", "r") as file:
    frames = json.load(file)
pygame.mixer.init()
pygame.mixer.music.load('audio.mp3')
pygame.mixer.music.play()
for k in range(len(frames)):
    sys.stdout.write(f"\033[{height}A")
    sys.stdout.write(f"\033[2K\r{frames[k]}")
    sys.stdout.flush()
    time.sleep(1.0/12.0)

