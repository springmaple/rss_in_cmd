import sys

import feedparser

from util import *

feeds = get_feeds_dict()


def check_all():
    read = get_read()
    for code, url in feeds.items():
        feed = feedparser.parse(url)
        last_read = read[code] if code in read else 0
        item_count = 0
        for item in feed['items']:
            published_time = to_unix_ts(item["published_parsed"])
            if last_read >= published_time:
                break
            item_count += 1
        print(f'  {item_count} from {code} since {to_pretty_date(last_read)}')


def check_one():
    code = sys.argv[1]
    read = get_read()
    last_read = read[code] if code in read else 0

    print(f'Fetching {code} since {to_pretty_date(last_read)}')
    print()
    feed = feedparser.parse(feeds[code])
    for item in feed['items']:
        published_time = to_unix_ts(item["published_parsed"])
        if last_read >= published_time:
            break

        print(f'  {item["title"]} - {item["link"]}')


def print_all_feeds():
    print()
    for feed_code in feeds.keys():
        print(f'  {feed_code}')


if len(sys.argv) < 2:
    check_all()
elif sys.argv[1] not in feeds.keys():
    print_all_feeds()
else:
    check_one()
