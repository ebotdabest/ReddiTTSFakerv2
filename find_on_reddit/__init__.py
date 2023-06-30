import os

import praw
import random

import console_api
from config import THREAD_DIR, SHOTS_DIR, API



reddit = praw.Reddit(client_id=API['id'],
                     client_secret=API["secret"],
                     user_agent=API['name'])

# print()
#
# # Get a list of all available subreddits
# all_subreddits = reddit.subreddit('all').subreddit(limit=None)


def get_thread_entire(name: str):
    subreddit = reddit.subreddit(name)

    random_thread = subreddit.random()

    if not random_thread.over_18:
        with open(f"{THREAD_DIR}/{random_thread.id}.json", "w") as f:
            import json
            data = {
                "title": random_thread.title,
                "id": random_thread.id,
                "url": random_thread.url,
                "body": random_thread.selftext
            }
            json.dump(data, f)
            os.mkdir(f"{SHOTS_DIR}/{random_thread.id}")
        return data
    else:
        return get_thread_entire(name)

def get_random_thread_by_name(name: str, amount: int):
    subreddit = reddit.subreddit(name)

    # Get a random submission from the subreddit
    random_thread = subreddit.random()
    # Print the thread title and URL
    console_api.print_msg(f"[blue]Trying thread[/blue] : [red]{random_thread.id}[/red]")
    # Get the comments for the thread
    comments = random_thread.comments
    if not random_thread.over_18:
        counter = 0
        if (len(comments) >= 10):
            from rich.table import Table
            console_api.print_msg(f"[red]Selected thread[/red] : [blue]{random_thread.title}[/blue]")
            # print("Selected thread:", random_thread.title)
            console_api.print_msg(f"[red]Selected thread url[/red] : [blue]{random_thread.url}[/blue]")
            # print("Selected thread url:", random_thread.url)
            table = Table(title="Comments")
            table.add_column("Author", style="red", justify="left")
            table.add_column("Comment text", style="green", justify="full")
            table.add_column("Author", style="blue", justify="right")
            comms = []
            for comment in comments:
                if counter != amount:
                    if comment.author is None:
                        pass
                    else:
                        table.add_row(comment.author.name, comment.body, str(comment.author))
                        comms.append(comment.body)
                        counter += 1

            with open(f"{THREAD_DIR}/{random_thread.id}.json", "w") as f:
                import json
                data = {
                    "title": random_thread.title,
                    "id": random_thread.id,
                    "url": random_thread.url,
                    "comments": comms
                }
                json.dump(data, f)
                os.mkdir(f"{SHOTS_DIR}/{random_thread.id}")
            console_api.print_msg(table)
            return data
        else:
            console_api.print_msg("Failed! Retrying...", style="red")
            # print("Failed! Retrying...")
            return get_random_thread_by_name(name, amount)
    else:
        console_api.print_msg("Failed! Retrying...", style="red")
        # print("Failed! Retrying...")
        return get_random_thread_by_name(name, amount)
