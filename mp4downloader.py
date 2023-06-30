from pytube import YouTube
from config import BG_DIR

link = input("Video link>>  ")
yt = YouTube(link)
print("Title: ",yt.title)
print("Number of views: ",yt.views)
print("Length of video: ",yt.length)
name = input("How to name the file>>  ")
description = input("Description>>  ")

ys = yt.streams.get_highest_resolution()

print("Downloading...")
ys.download(BG_DIR, f"{name}.mp4")
print("Download completed!!")

with open(BG_DIR + "/description.json", "r") as f:
    import json
    data: dict = json.load(f)


with open(BG_DIR + "/description.json", "w") as f:
    import json
    data[name + ".mp4"] = description
    json.dump(data, f)