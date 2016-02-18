This is the bot that is in use in #SecNews on 2600net.

To use this on your own network, follow the instructions below:

1. Move the 'secnews.py' file to your Cloudbot plugins directory.

2. Move the default 'feed_list.txt' file to your CloudBot data directory.

3. Add any extra feeds to 'feed_list.txt' by pasting them into the file, one per line.

4. Invite CloudBot into the channel you want secnews to message and type `.secnews start`.

You should immediately see a stream of rss feeds being output into the channel.

To stop it, type `.secnews stop`

If you want to test if the secnews plugin is working, type `.secnews debug`
