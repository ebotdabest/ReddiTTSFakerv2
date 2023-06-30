import os

import pyttsx3
from config import VOICES_DIR



def say_save(text, file, id):
    try:
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        rate = engine.getProperty('rate')
        nice = open(f"{VOICES_DIR}/{id}/{file}.mp3", "wb")
        nice.close()
        engine.setProperty('rate', 210)
        engine.save_to_file(text, f"{VOICES_DIR}/{id}/{file}.mp3")
        engine.runAndWait()
    except Exception as e:
        engine = pyttsx3.init()

        # Set the male voice
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 210)

        os.mkdir(f"{VOICES_DIR}/{id}")
        engine.save_to_file(text, f"{VOICES_DIR}/{id}/{file}.mp3")
        engine.runAndWait()