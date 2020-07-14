import json, collections

def get(file):
    # Credits: AlexFlipnote | https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/default.py
    try:
        with open(file, encoding = 'utf8') as data:
            return json.load(data, object_hook = lambda d: collections.namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown Argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON File wasn't found.")

def datefr(date, clock = True):
    return date.strftime("%A, %B %d %Y @ %H:%M:%S %p") if clock else date.strftime("%A, %B %d %Y")

def int_suffix(i):
    """Returns the ordinal representation of the given number."""
    return str(i) + {1: "st", 2: "nd", 3: "rd"}.get(i % 10 * (i % 100 not in {11, 12, 13}), "th")