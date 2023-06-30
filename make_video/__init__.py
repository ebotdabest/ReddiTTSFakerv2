import json
from typing import List

from moviepy.editor import *
from moviepy.editor import ImageClip
import os
from PIL import Image

import console_api
from config import VOICES_DIR, VIDEOS_DIR, SHOTS_DIR, IMGMAGICK_PATH, MUSIC_DIR, BG_DIR
from moviepy.audio.fx import volumex
from moviepy.audio.fx import audio_fadeout, audio_fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.resize import resize


def nice(video_bg, id, music, width, heigth, lengths):
    mp3_files = os.listdir(r"{}\{}".format(VOICES_DIR, id))

    saved = mp3_files[-1]
    mp3_files.remove("thread_mini.mp3")
    mp3_files.insert(0, saved)

    for x in range(len(mp3_files)):
        mp3_files[x] = f"{VOICES_DIR}/{id}/{mp3_files[x]}"
    # print(id)
    # print(SHOTS_DIR)
    # print(r"{}\{}".format(SHOTS_DIR, id))
    images = os.listdir(r"{}\{}".format(SHOTS_DIR, id))
    saved = images[-1]
    images.remove("thread_mini.png")
    images.remove("thread.png")
    images.insert(0, saved)
    for x in range(len(images)):
        if images[x] != "thread.png":
            images[x] = f"{SHOTS_DIR}/{id}/{images[x]}"

    audio_clips = [AudioFileClip(mp3_file) for mp3_file in mp3_files]

    clips_img = [Image.open(image) for image in images]

    for img in range(len(clips_img)):
        clips_img[img] = clips_img[img].resize((width, int(heigth / 8)))
        clips_img[img].save(images[img])

    image_clips = [ImageClip(image) for image in images]
    # Set the audio for each image
    for i, (audio_clip, image_clip) in enumerate(zip(audio_clips, image_clips)):
        image_clip.duration = audio_clip.duration
        image_clip.set_audio(audio_clip)
        image_clip = image_clip.set_audio(audio_clip)
        # image_clip.set_position("center")
        image_clips[i] = image_clip
        screen_width, screen_height = width, heigth

        # Set the position of the image
        image_clip.set_position((screen_width / 8, screen_height / 2))
        image_clips[i] = image_clip

    video = concatenate_videoclips(image_clips)
    new_video: VideoClip = CompositeVideoClip([video_bg, video])
    # print(new_video.audio)
    nice_xd = CompositeAudioClip([music, new_video.audio])
    new_video = new_video.set_audio(nice_xd)
    new_video.duration = sum(lengths)

    return new_video


voices = []


def add_voice(voice):
    voices.append(AudioFileClip(voice))


def set_durs():
    global counter


os.environ["IMAGEMAGICK_BINARY"] = IMGMAGICK_PATH


def choose(title):
    from rich.table import Table

    options = os.listdir(MUSIC_DIR)
    try:
        with open(f"{MUSIC_DIR}/description.json") as f:
            options.remove("description.json")
            descriptions = json.load(f)
    except FileNotFoundError:
        console_api.print_msg("Cannot find 'description.json' please create one and start the script again!",
                              style="red")
        exit()

    console_api.print_msg(f"[red]Title[/red] : [blue]{title}[/blue]")
    music_table = Table(title="Musics")

    music_table.add_column("Number", style="red", justify="right")
    music_table.add_column("Name", style="blue", justify="center")
    music_table.add_column("Description", style="yellow", justify="center")

    counter_xdxd = 0
    for music in options:
        music_table.add_row(str(counter_xdxd + 1), music.strip().split(".")[0], descriptions[music])
        counter_xdxd += 1

    console_api.print_msg(music_table)

    music_selection = int(console_api.input_txt("[green]Which music would you like for this thread?>>[/green]  "))
    console_api.print_msg(f"[red]You choose[/red] : [blue]{options[music_selection - 1]}[/blue]")
    try:
        audio = AudioFileClip(f"{MUSIC_DIR}/{options[music_selection - 1]}")
        audio: AudioClip = volumex.volumex(audio, 0.3)

    except Exception:
        music_selection = int(console_api.input_txt("[green]Which music would you like for this thread?>>[/green]  "))
        console_api.print_msg(f"[red]You choose[/red] : [blue]{options[music_selection - 1]}[/blue]")
        audio = AudioFileClip(f"{MUSIC_DIR}/{options[music_selection - 1]}")
        audio: AudioFileClip = volumex.volumex(audio, 0.3)

    # audio = audio_fadein.audio_fadein(audio, 0.5)
    # audio = audio_fadeout.audio_fadeout(audio, 2)

    # Video
    vidoptions = os.listdir(BG_DIR)
    try:
        with open(f"{BG_DIR}/description.json") as f:
            vidoptions.remove("description.json")
            descriptions = json.load(f)
    except FileNotFoundError:
        console_api.print_msg("Cannot find 'description.json' please create one and start the script again!",
                              style="red")
        exit()

    console_api.print_msg("Video options", style="blue")
    del counter_xdxd

    vid_table = Table(title="Videos")

    vid_table.add_column("Number", style="red", justify="right")
    vid_table.add_column("Name", style="blue", justify="center")
    vid_table.add_column("Description", style="yellow", justify="center")

    counter_xdxd = 0
    for video in vidoptions:
        vid_table.add_row(str(counter_xdxd + 1), video.strip().split(".")[0], descriptions[video])
        counter_xdxd += 1
    console_api.print_msg(vid_table)

    video_selection = int(console_api.input_txt("[green]Which video would you like for this thread?>>[/green]  "))
    try:
        video = VideoFileClip(f"{BG_DIR}/{vidoptions[video_selection - 1]}")
        # audio: AudioClip = volumex.volumex(audio, 0.3)

    except Exception as e:
        video_selection = int(console_api.input_txt("[green]Which video would you like for this thread?>>[/green]  "))
        console_api.print_msg(f"[red]You choose[/red] : [blue]{options[video_selection - 1]}[/blue]")
        video = VideoFileClip(f"{BG_DIR}/{vidoptions[video_selection - 1]}")
        # audio: AudioClip = volumex.volumex(audio, 0.3)

    console_api.print_msg(f"[red]You choose[/red] : [blue]{options[video_selection - 1]}[/blue]")

    console_api.print_msg(f"[red]Music[/red] : [blue]{options[music_selection - 1]}[/blue]")
    console_api.print_msg(f"[red]Video[/red] : [blue]{vidoptions[video_selection - 1]}[/blue]")
    choice = console_api.input_txt("[blue]Is it correct?[/blue] <Y/N>  ")
    if choice.lower() == "y":
        return {"audio": audio, "video": video}
    elif choice.lower() == "n":
        return choose(title)
    else:
        console_api.print_msg("[red]Cannot understand, understood : 'NO'![/red]")
        return choose(title)


# def put_in():
#

def very_keksz():
    pass


def create(id: str, title, type, subreddit):
    global voices

    if type == 0:
        path = f"{VOICES_DIR}/{id}/"
        path2 = f"{SHOTS_DIR}/{id}/"
        mp3_files = [f for f in os.listdir(path) if f.endswith('.mp3')]
        imgs = [f for f in os.listdir(path2) if f.endswith(".png") and f != "thread.png"]
        saved = imgs[-1]
        imgs.remove(imgs[-1])
        # imgs.remove(imgs[-1])
        imgs.insert(0, saved)
        lengths = []
        mp3_files.insert(0, mp3_files[-1])
        for mp3 in mp3_files:
            clip = AudioFileClip(path + mp3)
            lengths.append(clip.duration)
            clip.close()

        for x in range(len(imgs)):
            imgs[x] = f"{SHOTS_DIR}/{id}/{imgs[x]}"

        dat = choose(title)

        audio = dat["audio"]
        video = dat["video"]

        nice_video = nice(video, id, audio, video.w, video.h, lengths)
        # nice_video.set_audio(CompositeAudioClip([audio, audio_clip]))
        nice_video.duration = sum(lengths)
        nice_video = nice_video.set_duration(sum(lengths) - 2)
        os.mkdir(f"{VIDEOS_DIR}/{id}")
        nice_video = fadein(nice_video, 0.5)
        nice_video = fadeout(nice_video, 2)
        nice_video.write_videofile(f"{VIDEOS_DIR}/{id}/video.mp4")
        with open(f"{VIDEOS_DIR}/{id}/summary.json", "w") as f:
            json.dump({
                "audio": audio.filename,
                "video": video.filename,
                "subreddit": subreddit,
                "title": title
        }, f)
    elif type == 1:
        dat = choose(title)
        bg_audio = dat["audio"]
        bg_video = dat["video"]

        title_audio = AudioFileClip(f"{VOICES_DIR}/{id}/title.mp3")
        body_audio = AudioFileClip(f"{VOICES_DIR}/{id}/body.mp3")

        thread_img = ImageClip(f"{SHOTS_DIR}/{id}/thread.png")
        screen_width, screen_height = bg_video.w, bg_video.h / 8
        thread_img = resize(thread_img, (screen_width, thread_img.h))
        # Set the position of the image
        thread_img = thread_img.set_position("top")

        thread_img = thread_img.set_audio(concatenate_audioclips([title_audio, body_audio]))

        bg_video = bg_video.set_audio(bg_audio)

        video = CompositeVideoClip([bg_video, thread_img])

        video = video.set_duration(sum([title_audio.duration, body_audio.duration]))

        video = fadein(video, 0.5)
        video = fadeout(video, 2)



        os.mkdir(f"{VIDEOS_DIR}/{id}")
        video.write_videofile(f"{VIDEOS_DIR}/{id}/video.mp4")
        with open(f"{VIDEOS_DIR}/{id}/summary.json", "w") as f:
            json.dump({
                "audio": bg_audio.filename,
                "video": bg_video.filename,
                "subreddit": subreddit,
                "title": title
        }, f)