import feedparser
import os
import asyncio
import threading
from time import sleep

from cloudbot import hook
from cloudbot.util import web, formatting

SLEEP_TIME = 300 # Time to sleep before pulling feeds, in secs
FEED_LIST = []  # List of feeds to parse from feed_list.txt
LAST_STORIES = []   # Links to last stories printed

IS_RUNNING = False  # Boolean switch to kill secnews thread

def async_secnews(message):
    while(IS_RUNNING):
        for feed in FEED_LIST:
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
                            message("Title:     {}".format(entry.title))
                            sleep(1)
                        except AttributeError:
                            pass
                        try:
                            message("Summary:   {}".format(entry.summary))
                            sleep(1)
                        except AttributeError:
                            pass
                        try:
                            message("Published: {}".format(entry.published))
                            sleep(1)
                        except AttributeError:
                            pass
                        message("{}".format(link))
                        sleep(1)
                        message("-----------------------------------------------------")
                        sleep(1)
                        LAST_STORIES.append(link)
                        # Prevent LAST_STORIES from getting too full...
                        if len(LAST_STORIES) >= 2600:
                            LAST_STORIES.pop(0)
                    # Check for kill signal to prevent spam and end if received
                    if not IS_RUNNING:
                        return 
        sleep(SLEEP_TIME)
            

@hook.on_start()
def load_feeds(bot):
    global FEED_LIST
    with open(os.path.join(bot.data_dir, 'feed_list.txt')) as f:
        FEED_LIST = f.readlines()


@asyncio.coroutine
@hook.command(permissions=['botcontrol'])
def secnews(text, message):
    """<add|del> <feed> -- Add/Delete a feed from the feed_list."""
    global IS_RUNNING
    args = text.strip().split()
    if args[0].lower() == 'add':
        FEED_LIST.append(args[1])
        message("'{}' added to the feed list.".format(args[1]))
    elif args[0].lower() == 'del':
        try:
            FEED_LIST.remove(args[1])
        except ValueError:
            message("'{}' was not found in the feed list.".format(args[1]))
    elif args[0].lower() == 'start':
        secnews_thread = threading.Thread(None, async_secnews, args=[message])
        IS_RUNNING = True
        secnews_thread.start()
    elif args[0].lower() == 'stop':
        IS_RUNNING = False
    elif args[0].lower() == 'debug':
        message("I'm here - #secnews")
