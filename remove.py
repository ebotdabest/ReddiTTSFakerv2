import os
from config import *
ID = "107i910"
os.removedirs(f"{SHOTS_DIR}/{ID}")
os.removedirs(f"{VOICES_DIR}/{ID}")
os.removedirs(f"{VIDEOS_DIR}/{ID}")
os.remove(f"{THREAD_DIR}/{ID}.json")