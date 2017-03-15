import feedparser
from bot import Bot
import configparser
import sched
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--ini')
args = parser.parse_args()
config_file = args.ini if args.ini is not None else 'config.ini'

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
config = configparser.ConfigParser()
config.read(os.path.join(__location__, config_file))

URL = config['RSSFeed']['URL']
UPDATE_TIMEOUT = config.getint('RSSFeed', 'update_timeout')
bot = Bot(config)


def check_updates():
    feed = feedparser.parse(URL)
    last_id_file = os.path.join(__location__, 'last_id')
    with open(last_id_file, 'r') as f:
        last_id = f.read()
        print(last_id)

    theme_id = None
    new_themes = []
    for topic in feed.entries:
        theme_id = topic.id
        if topic.id == last_id or len(last_id) == 0:
            break
        else:
            new_themes.append(topic)

    print('new themes:', new_themes)

    for topic in reversed(new_themes):
        theme_url = topic.link
        theme_title = topic.title
        theme_content = topic.description
        bot.send_message(theme_title, theme_content, theme_url)

    if theme_id is not None:
        with open(last_id_file, 'w') as f:
            f.write(feed.entries[0].id)


def scheduled_update(sched):
    check_updates()
    sched.enter(UPDATE_TIMEOUT, 1, scheduled_update, (sched,))


def run_forever():
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, scheduled_update, (scheduler,))
    scheduler.run()

run_forever()
