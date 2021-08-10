import datetime
import discord
import logging
import requests
import shutil
import tempfile

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
    results = data["results"]
    top_result = results[0]
    embed.title = top_result["title"]
    embed.description = top_result["titletext"]
    embed.timestamp = datetime.datetime.strptime(
        top_result["date"], "%Y-%m-%d"
    )
    embed.set_footer(text=f"https://{top_result['url']}")
    other_results = "\n".join(
        [
            f"- [{result['title']}](https://{result['url']})"
            for result in results[1:6]
        ]
    )
    embed.add_field(name="Similar Results", value=other_results)
    with tempfile.NamedTemporaryFile() as fp:
        img = requests.get(top_result["image"], stream=True)
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, fp)
        await ctx.send(
            file=discord.File(fp.name, filename=top_result["image"]),
            embed=embed,
        )
