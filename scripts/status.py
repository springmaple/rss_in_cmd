import sys
from concurrent.futures.thread import ThreadPoolExecutor

import feedparser

from util import *

feeds = get_feeds_dict()


def check_all():
    read = get_read()
    executor = ThreadPoolExecutor(max_workers=10)

    def load(code, url):
        feed = feedparser.parse(url)
        if feed['bozo'] != 0:
            print(f'Failed to load feeds from {code}')
            return

        last_read = read[code] if code in read else 0
        item_count = 0
        for item in feed['items']:
            published_time = to_unix_ts(item["published_parsed"])
            if last_read >= published_time:
                break
            item_count += 1
        print(f'{item_count} from {code} since {to_pretty_date(last_read)}')

    for c, u in feeds.items():
        executor.submit(load, c, u)

    executor.shutdown(wait=True)


def check_one():
    code = sys.argv[1]
    read = get_read()
    last_read = read[code] if code in read else 0

    feed = feedparser.parse(feeds[code])
    if feed['bozo'] == 0:
        def date_filter(itm):
            return last_read < to_unix_ts(itm["published_parsed"])

        items = list(filter(date_filter, feed['items']))
        print(f'{len(items)} new items since at {to_pretty_date(last_read)}')
        if len(items) > 0:
            print()
            for index, item in enumerate(items):
                print(f'  {index + 1}. {item["title"]} - {item["link"]}')
    else:
        print(f'Failed to load feeds from {code}')


if len(sys.argv) < 2:
    check_all()
elif sys.argv[1] not in feeds.keys():
    print_all_feeds(feeds)
else:
    check_one()
