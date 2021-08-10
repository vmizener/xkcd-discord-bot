import os
from xkcdbot import bot

token = os.environ.get("BOT_TOKEN")


if __name__ == "__main__":
    bot.run(token)
