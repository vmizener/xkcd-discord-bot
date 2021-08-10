import os

BOT_DESCRIPTION = os.environ.get(
    "BOT_DESCRIPTION", "Bot for retrieving XKCD comic strips"
)
COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", "xkcd ")
