from pytube import YouTube
from config import MUSIC_DIR


link = input("Music link>>  ")
yt = YouTube(link)
print("Title: ",yt.title)
print("Number of views: ",yt.views)
print("Length of video: ",yt.length)
name = input("How to name the file>>  ")
description = input("Description>>  ")
ys = yt.streams.get_audio_only()

print("Downloading...")
ys.download(MUSIC_DIR, f"{name}.mp3")
print("Download completed!!")
with open(MUSIC_DIR + "/description.json", "r") as f:
    import json
    data: dict = json.load(f)


with open(MUSIC_DIR + "/description.json", "w") as f:
    import json
    data[name + ".mp3"] = description
    json.dump(data, f)