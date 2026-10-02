import sys
import subprocess
import cv2
import numpy as np
import time
import os
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import moviepy as mp

STEP = 32
repeated=False

scale = np.array(list("$@B%8&WM#*oahkbdpqwmZO0QLC()1{}[]?-_+~<>i!lI;:,\"^`"))

width = int(subprocess.check_output(["tput", "cols"]))-1
height = int(subprocess.check_output(["tput", "lines"]))-1

videoname=sys.argv[1]
video = cv2.VideoCapture(videoname)
original_fps = video.get(cv2.CAP_PROP_FPS)
vidlen=int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_step = max(1, (int(original_fps/12) if original_fps%12<6 else int(original_fps/12)+1))
effective_fps = original_fps / frame_step
fname=os.path.splitext(videoname)[0]+"_"+str(width)+","+str(height)+"_"+str(STEP)+".cache"
print("Video file found")
pygame.mixer.init()

def get_audio_sound_object(video_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    if video.audio is not None:
        audio.write_audiofile("audio.mp3",logger=None)
        audio.close()

    video.close()
    print("Audio file extracted successfully")
    return
def makeframes(frame_id=0):
    with open(fname, "wb") as file:
        while True:
            success, image = video.read()
            if not success:
                break
            if frame_id % frame_step == 0:
                percentage=int(frame_id/vidlen*100)
                sys.stdout.write("\rConverting frames to ascii [" + int(percentage/10)*"#"+"-"+(9-int(percentage/10))*" "+"]"+f" {percentage}%")
                sys.stdout.flush()
                resized = cv2.resize(image, (width+1 , height+1 ), interpolation=cv2.INTER_AREA)
                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                lum = (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2])
                ind = (lum / 255.0 * (len(scale) - 1)).astype(int)
                chars = scale[ind]

                q = (rgb // STEP * STEP + STEP // 2).clip(0, 255).astype(np.uint8)
                key = (q[:, :, 0].astype(np.uint32) << 16) | (q[:, :, 1].astype(np.uint32) << 8) | q[:, :, 2]
                changed = np.ones(key.shape, dtype=bool)
                changed[:, 1:] = key[:, 1:] != key[:, :-1]

                esc = ("\033[38;2;" + q[:, :, 0].astype(str) + ";" + q[:, :, 1].astype(str)+ ";" + q[:, :, 2].astype(str) + "m")
                esc = np.where(changed, esc, "")
                grid = np.char.add(esc, chars)
                output = "\033[H" + "\n".join("".join(row) for row in grid)
                data = output.encode("utf-8")
                file.write(len(data).to_bytes(4, "little"))
                file.write(data)
            frame_id += 1
get_audio_sound_object(videoname)
print('\n')
if not os.path.exists(fname):
    makeframes()

pygame.mixer.music.load("audio.mp3")
pygame.mixer.music.play()
with open(fname, "rb") as file:
    while True:
        size_bytes = file.read(4)
        if not size_bytes:
            break
        size = int.from_bytes(size_bytes, "little")
        data = file.read(size)
        frame = data.decode("utf-8")
        sys.stdout.write(f"\033[{height}A")
        sys.stdout.write(f"\r{frame}")
        sys.stdout.flush()
        time.sleep(1.0 / effective_fps)


