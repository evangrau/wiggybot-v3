from discord.ext import commands
import requests
import random
from settings import ADMIN_IDS
from loguru import logger as log

WIGGY_ID = ADMIN_IDS[0]

@commands.hybrid_command(name="joke", description="Get a random joke.")
async def joke(ctx : commands.Context):
    """Gets a random joke"""

    log.info("Running joke command...")

    headers = {
        "Accept": "application/json" 
    }

    c = [0,1]
    type = random.choice(c)

    if type == 0:
        url = "https://icanhazdadjoke.com"
    else:
        url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist"

    try:
        r = requests.get(url, headers=headers)
        res = r.json()

        if type == 0:
            await ctx.send(res["joke"])
        else:
            if res["type"] == "twopart":
                await ctx.send(f"{res['setup']}\n||{res['delivery']}||")
            else:
                await ctx.send(res["joke"])
    except Exception as e:
        await ctx.send(f"An error occurred while fetching a joke. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")
        log.error(f"An error occurred while fetching a joke: {e}")

async def setup(bot):
    bot.add_command(joke)