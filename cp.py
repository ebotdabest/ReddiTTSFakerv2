from functions import create_preset
import console_api as ca


subreddit = ca.input_txt("Which subreddit do you want?>>  ")
name = ca.input_txt("Name of the preset>>  ")
comment_amount = ca.input_txt("How much comments>>  ")
toc = ca.input_txt("Threads or comments?>>  ")

create_preset(subreddit, name, comment_amount, toc)
