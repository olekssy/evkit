""" General purpose and auxiliary functions """

import json

# -------------------- Global Variables --------------------
PATH_CONFIG_FILE = "evkit/settings.json"


def load_config():
    """ Load configs from json """
    with open(PATH_CONFIG_FILE, "r") as file:
        configs = json.load(file)
    return configs
