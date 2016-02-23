import feedparser
import os
import asyncio
import threading
from time import sleep

from cloudbot import hook
from cloudbot.util import web, formatting

from lxml import html
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

SLEEP_TIME = 300 # Time to sleep before pulling feeds, in secs
FEED_LIST = {}  # List of feeds to parse from feed_list.yml
LAST_STORIES = []   # Links to last stories printed

IS_RUNNING = False  # Boolean switch to kill tuxnews thread

def async_tuxnews(message, chan):
    while(IS_RUNNING):
        for feed in FEED_LIST[chan[1:]]:
            news = feedparser.parse(feed)
            for entry in news.entries:
                try:
                    # Check that a readable story is in the feed
                    link = entry.link
                except AttributeError:
                    pass
                else:
                    # Do not print stories that have been already printed
                    if not link in LAST_STORIES:
                        try:
                            message("Title:     \x02{}".format(entry.title))
                            sleep(1)
                        except AttributeError:
                            pass
                        message("\x1f{}".format(link))
                        sleep(1)
                        try:
                            summary = html.fromstring(entry.summary)\
                                    .text_content()
                            message("Summary:   {}".format(summary))
                            sleep(1)
                        except AttributeError:
                            pass
                        message("---------------------------------------------"\
                                "----------")
                        sleep(1)
                        LAST_STORIES.append(link)
                        # Prevent LAST_STORIES from getting too full...
                        if len(LAST_STORIES) >= 2600:
                            LAST_STORIES.pop(0)
                    # Check for kill signal to prevent spam
                    if not IS_RUNNING:
                        return 
        sleep(SLEEP_TIME)
            

@hook.on_start()
def load_feeds(bot):
    global FEED_LIST
    with open(os.path.join(bot.data_dir, 'feed_list.yml')) as f:
        FEED_LIST = load(f, Loader=Loader)


@asyncio.coroutine
@hook.command(permissions=['botcontrol'])
def tuxnews(text, message, chan, bot):
    """<start|reload(add|del> <feed>)"""
    global IS_RUNNING
    args = text.strip().split()
    if args[0].lower() == 'add':
        if not chan[1:] in FEED_LIST:
            FEED_LIST[chan[1:]] = []
        if not args[1] in FEED_LIST[chan[1:]]:
            FEED_LIST[chan[1:]].append(args[1])
            message("'{}' added to the feed list for this channel."\
                    .format(args[1]))
        else:
            message("'{}' already in the feed list for this channel."\
                    .format(args[1]))
    elif args[0].lower() == 'del':
        try:
            FEED_LIST[chan[1:]].remove(args[1])
            message("'{}' removed from the feed list for this channel."\
                    .format(args[1]))
        except ValueError:
            message("'{}' was not found in the feed list for this channel."\
                    .format(args[1]))
    elif args[0].lower() == 'start':
        if chan[1:] in FEED_LIST:
            tuxnews_thread = threading.Thread(None, async_tuxnews,\
                    args=[message, chan])
            IS_RUNNING = True
            tuxnews_thread.start()
        else:
            message("No default feeds found for this channel.")
    elif args[0].lower() == 'stop':
        IS_RUNNING = False
    elif args[0].lower() == 'reload':
        load_feeds(bot)
