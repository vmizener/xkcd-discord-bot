import datetime
import discord
import logging
import requests
import shutil
import tempfile

from discord.ext import commands
from .config import BOT_DESCRIPTION, COMMAND_PREFIX

INFO_RELEVANT_XKCD = "https://relevant-xkcd.github.io"
INFO_GITHUB = "https://github.com/vmizener/xkcd-discord-bot"
RELEVANT_XKCD_URL = "https://relevant-xkcd-backend.herokuapp.com/search"

logging.basicConfig()
log = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=BOT_DESCRIPTION)


@bot.command()
async def search(ctx, args):
    embed = discord.Embed()
    resp = requests.post(RELEVANT_XKCD_URL, data={"search": args})
    fail_msg, failed = "", False
    if not resp.ok:
        fail_msg = "Failed to receive response from relevant-xkcd"
        failed = True
    data = resp.json()
    if not data["success"]:
        fail_msg = "Relevant-xkcd reported bad result"
        failed = True
    results = data["results"]
    if len(results) == 0:
        fail_msg = "Somehow, there aren't any relevant XKCDs for that"
        failed = True
    if failed:
        log.error(f"{fail_msg}; args: {args}")
        await ctx.reply(fail_msg)
        return
    top_result = results[0]
    log.info(f"[{top_result['title']}]({top_result['url']})")
    embed.title = f"{top_result['number']}: {top_result['title']}"
    embed.description = (
        f"[{top_result['titletext']}](https://{top_result['url']})"
    )
    embed.timestamp = datetime.datetime.strptime(
        top_result["date"], "%Y-%m-%d"
    )
    if len(results) > 1:
        other_results = "\n".join(
            [
                f"- [{result['title']}](https://{result['url']})"
                for result in results[1:6]
            ]
        )
        embed.add_field(name="Similar Results", value=other_results)
    embed.add_field(
        name="Bot Info",
        value=f"- [Relevant-XKCD]({INFO_RELEVANT_XKCD})\n- [Github]({INFO_GITHUB})",
    )
    with tempfile.NamedTemporaryFile() as fp:
        img = requests.get(top_result["image"], stream=True)
        img.raw.decode_content = True
        shutil.copyfileobj(img.raw, fp)
        await ctx.reply(
            file=discord.File(fp.name, filename=top_result["image"]),
            embed=embed,
        )
