import os
import json
import pathlib
import logging
from client.utils import ReadOnlyDict


CONFIG_FILE = "conf.json"

BASE_DIR = pathlib.Path(__file__).resolve().parent

CONFIG_PATH = os.path.join(BASE_DIR, CONFIG_FILE)


def get_config():
    config = get_default_config()

    if not os.path.exists(CONFIG_PATH):
        logging.warning(f"Path to config file '{CONFIG_FILE}' was not found. Using default configuration.")
        return config

    with open(CONFIG_FILE, "r") as f:
        config.update(json.load(f))

    return ReadOnlyDict(config)


def get_default_config():
    return {"meta_host": "127.0.0.1", "meta_port": "8080", "block_size": 4096}
