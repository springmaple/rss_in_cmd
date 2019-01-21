from datetime import datetime
import json
import os
from time import mktime

with open(r'../settings.json', mode='r') as sf:
    SETTINGS = json.load(sf)

DATA_DIR = SETTINGS['data_dir']
RSS_ENTRIES = os.path.abspath(os.path.join(DATA_DIR, r'entries.json'))
READ_CACHE = os.path.abspath(os.path.join(DATA_DIR, r'read.json'))


def to_unix_ts(time_structure):
    # https://stackoverflow.com/a/1697907/1640033
    return mktime(time_structure)


def to_pretty_date(timestamp):
    return datetime.fromtimestamp(timestamp)


def get_feeds():
    with open(RSS_ENTRIES, mode='r') as f:
        return json.load(f) or []


def get_feeds_dict():
    return {item['code']: item['url'] for item in get_feeds()}


def get_read():
    if os.path.exists(READ_CACHE):
        with open(READ_CACHE, mode='r') as f:
            return json.load(f) or {}
    return {}


def save_read(read):
    with open(READ_CACHE, mode='w') as f:
        json.dump(read, f, indent=2)
