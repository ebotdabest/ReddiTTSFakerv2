import json
import os

import prawcore.exceptions

from config import *
from find_on_reddit import get_random_thread_by_name, get_thread_entire
from collect_data import get_mugshot_by_url, removed, get_threadshot_by_url
from tts import say_save
from make_video import add_voice, create
import console_api as ca
import sys
from functions import load_preset
from youtube_upload_test import upload

preset = None
for arg in sys.argv:
    if "-preset" in arg:
        preset = arg.split("=")[1]




if preset != None:
    da = load_preset(preset.split(".")[0])
    AMOUNT = int(da["am"])
    subreddit = da["sub"]
    TYPE = int(da["tp"])
    n = da["pname"]
    ca.print_msg(f"[red]Loaded preset[/red] : [blue]{n}[/blue]")
else:
    subreddit = str(ca.input_txt("Which subbreddit do you want?>>  "))
    type_val = ca.input_txt("Do you want comments or thread? (c/t)>>  ")
    if type_val.lower() == "c":
        TYPE = 0
        AMOUNT = int(ca.input_txt("How much comments do you want? [red][Do not got over 8][/red]>>  "))

    elif type_val.lower() == "t":
        TYPE = 1
        # return {"subreddit": subreddit, "type": TYPE}
    else:
        ca.print_msg("Sorry I cannot understand it. Trying again..", style="red")
        # return choose()


    # comments_post = str(input("Do you want the thread or the commands?>>  "))
if TYPE == 0:
    try:
        data = get_random_thread_by_name(subreddit, AMOUNT)
    except prawcore.exceptions.ResponseException:
        ca.print_msg("Error, the API config is invalid", style="red")
        exit()

    def contains_element(list1, list2):
        return any(elem in list2 for elem in list1)


    url = data["url"]
    id = data["id"]
    title = data["title"]
    comments = data["comments"]
    del data


    # print("Working with id {}".format(id))
    ca.print_msg(f"[red]Working with id[/red] : [blue]{id}[/blue]")
    get_mugshot_by_url(url, AMOUNT, id)

    say_save(title, "thread_mini", id)

    files = os.listdir(f"{VOICES_DIR}/{id}")
    for file in files:
        add_voice(f"{VOICES_DIR}/{id}/{file}")

    create(id, title, 0, subreddit)

    ca.print_msg(f"[green]Done! With thread id[/green] : [blue]{id}[/blue]")

    ca.print_msg("Opening...", style="green")

    os.system(r"start explorer {}\{}".format(VIDEOS_DIR, id))

    doupload = ca.input_txt("Would you like to upload this video (Y/N)")

    if doupload.lower() == "y":
        with open(r"{}\{}\summary.json".format(VIDEOS_DIR, id)) as f:

            d = json.load(f)

            name = "r/" + d["subreddit"] + " - " + d["title"]
            description = "Music: " + d["audio"].split("/")[1].replace(".mp3", "")

            vis = ca.input_txt("What visibility do you want?")

        upload(name, description, [], vis, r"{}\{}\video.mp4".format(VIDEOS_DIR, id))
    else:
        ca.print_msg("Goody bye!")
        exit()

    # os.system(r"start explorer {}\{}\video.mp4".format(VIDEOS_DIR, id))
elif TYPE == 1:
    try:
        data = get_thread_entire(subreddit)
        url = data["url"]
        id = data["id"]
        title = data["title"]
        body = data["body"]
        del data

        ca.print_msg(f"[red]Working with id[/red] : [blue]{id}[/blue]")

        get_threadshot_by_url(url, id)

        ca.print_msg("Saying title", "blue")
        ca.print_msg("Saying body", "blue")

        say_save(title, "title", id)
        say_save(body, "body", id)

        create(id, title, 1, subreddit)

        ca.print_msg("Opening...", style="green")

        os.system(r"start explorer {}\{}".format(VIDEOS_DIR, id))

        # doupload = ca.input_txt("Would you like to upload this video (Y/N)>>  ")
        #
        #
        # if doupload.lower() == "y":
        #     with open(r"{}\{}\summary.json".format(VIDEOS_DIR, id)) as f:
        #
        #         d = json.load(f)
        #
        #         name = "r/" + d["subreddit"] + " - " + d["title"]
        #         description = "Music: " + d["audio"].split("/")[1]
        #
        #         vis = ca.input_txt("What visibility do you want? (public/mid/private)>>  ")
        #
        #     upload(name, description, [], vis, r"{}\{}\video.mp4".format(VIDEOS_DIR, id))
        # else:
        #     ca.print_msg("Goody bye!")
        #     exit()
    except prawcore.exceptions.ResponseException:
        ca.print_msg("Error, the API config is invalid", style="red")
        exit()