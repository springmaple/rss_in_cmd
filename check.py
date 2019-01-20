import json
import os
from time import mktime

import feedparser

RSS_ENTRIES = r'entries.json'
READ_CACHE = r'read.json'


def to_unix_ts(time_structure):
    # https://stackoverflow.com/a/1697907/1640033
    return mktime(time_structure)


if not os.path.exists(RSS_ENTRIES):
    exit()

with open(RSS_ENTRIES, mode='r') as f:
    entries = json.load(f)

if os.path.exists(READ_CACHE):
    with open(READ_CACHE, mode='r') as f:
        read = json.load(f) or {}
else:
    read = {}

last_read = {}
for code, url in {item.get('code'): item.get('url') for item in entries}.items():
    print(f'Checking {code}')
    feed = feedparser.parse(url)
    for item in feed['items']:
        published_time = to_unix_ts(item["published_parsed"])
        if code in read and read[code] >= published_time:
            break

        print(f'{item["title"]} - {item["link"]}')
        if code not in last_read or published_time > last_read[code]:
            last_read[code] = published_time

    print()

for code, updated_time in last_read.items():
    if code not in read or updated_time > read[code]:
        read[code] = updated_time

with open(READ_CACHE, mode='w') as f:
    json.dump(read, f, indent=2)
