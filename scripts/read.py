from util import *
import sys
import feedparser

feeds = get_feeds_dict()


def print_all_feeds():
    print()
    for feed_code in feeds.keys():
        print(f'  {feed_code}')


def mark_read():
    code = sys.argv[1]
    read = get_read()
    feed = feedparser.parse(feeds[code])
    items = feed['items']
    if len(items) > 0:
        latest_item = items[0]
        published_time = to_unix_ts(latest_item["published_parsed"])
        if code not in read or published_time >= read[code]:
            read[code] = published_time
            save_read(read)
            print(f'Marked last read of {code} to {to_pretty_date(published_time)}.')
            return
        print(f'Last read of {code} is later than current last item.')
        return
    print(f'{code} has no item.')


if len(sys.argv) < 2 or sys.argv[1] not in feeds:
    print_all_feeds()
else:
    mark_read()
