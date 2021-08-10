import datetime
import discord
import logging
import requests

from discord.ext import commands
from .config import BOT_DESCRIPTION, COMMAND_PREFIX

RELEVANT_XKCD_URL = "https://relevant-xkcd-backend.herokuapp.com/search"

logging.basicConfig()
log = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=BOT_DESCRIPTION)


@bot.command()
async def search(ctx, args):
    embed = discord.Embed()
    resp = requests.post(RELEVANT_XKCD_URL, data={"search": args})
    if not resp.ok:
        log.error("err1")
    data = resp.json()
    if not data["success"]:
        log.error("err2")
    top_result = data["results"][0]
    embed.title = top_result["title"]
    embed.description = top_result["titletext"]
    embed.timestamp = datetime.datetime.strptime(
        top_result["date"], "%Y-%m-%d"
    )
    embed.set_image(url=top_result["image"])
    embed.set_footer(text=top_result["url"])
    await ctx.send(embed=embed)
