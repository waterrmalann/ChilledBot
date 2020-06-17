# Credits to AlexFlipnote for the get() function.
# https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/default.py

import json, collections

def get(file):
    try:
        with open(file, encoding = 'utf8') as data:
            return json.load(data, object_hook = lambda d: collections.namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown Argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON File wasn't found.")
