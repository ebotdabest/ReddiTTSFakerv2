import os
import os.path as path
from config import VOICES_DIR, VIDEOS_DIR, SHOTS_DIR, THREAD_DIR

for stuff in os.listdir(THREAD_DIR):
    os.remove(f"{THREAD_DIR}/{stuff}")
    print("Deleted:", stuff)

try:
    for stuff in os.listdir(SHOTS_DIR):
        for shit_content in os.listdir(f"{SHOTS_DIR}/{stuff}"):
            os.remove(f"{SHOTS_DIR}/{stuff}/{shit_content}")
        os.removedirs(f"{SHOTS_DIR}/{stuff}/")
        print("Deleted:", stuff)
except Exception:
    pass

try:
    os.mkdir("shots")
except FileExistsError:
    pass

for stuff in os.listdir(VIDEOS_DIR):
    for shit_content in os.listdir(f"{VIDEOS_DIR}/{stuff}"):
        os.remove(f"{VIDEOS_DIR}/{stuff}/{shit_content}")
    os.removedirs(f"{VIDEOS_DIR}/{stuff}/")
    print("Deleted:", stuff)

try:
    os.mkdir("videos")
except FileExistsError:
    pass

for stuff in os.listdir(VOICES_DIR):
    if path.isdir(f"{VOICES_DIR}/{stuff}"):
        for shit_content in os.listdir(f"{VOICES_DIR}/{stuff}"):
            os.remove(f"{VOICES_DIR}/{stuff}/{shit_content}")
    if not path.isfile(f"{VOICES_DIR}/{stuff}/"):
        if path.isfile(f"{VOICES_DIR}/{stuff}"):
            pass
        else:
            os.removedirs(f"{VOICES_DIR}/{stuff}/")
            print("Deleted:", stuff)
try:
    os.mkdir("voices")
except FileExistsError:
    pass
