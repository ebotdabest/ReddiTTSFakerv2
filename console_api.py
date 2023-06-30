from rich.console import Console

con = Console()

def set_title(new: str):
    con.set_window_title(new)

def print_msg(msg, style = ""):
    con.print(msg, style=style)

def input_txt(msg):
    return con.input(msg)
