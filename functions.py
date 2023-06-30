def load_preset(name):
    dat = {}
    with open(name + ".ftts") as f:
        nice = f.read().strip().split("\n")

    for stuff in nice:
        if stuff == "{" or stuff == "}":
            nice.remove(stuff)

    for stuff in nice:
        stuff = stuff.strip().split("  ")
        dat[stuff[0].replace("'", "").replace('"', "")] = stuff[1].replace("'", "").replace('"', "")

    return dat


def create_preset(sr, name, amount, type):
    dat = {
        "sub": sr,
        "pname": name,
        "amount": amount,
        "type": type
    }

    with open(name + ".ftts", "w") as f:
        f.write("{\n"
                f'    "sub"  "{dat["sub"]}"\n'
                f'    "pname"  "{dat["pname"]}"\n'
                f'    "am"  "{dat["amount"]}"\n'
                f'    "tp"  "{dat["type"]}"\n'
                "}\n")
