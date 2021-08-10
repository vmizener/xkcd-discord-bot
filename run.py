#!/usr/bin/env python3
import os
from xkcdbot import bot

# TODO: throw relevant warning if token isn't set
token = os.environ.get("BOT_TOKEN")


if __name__ == "__main__":
    bot.run(token)
