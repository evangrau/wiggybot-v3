import discord
from discord import app_commands
import requests
import random
from loguru import logger as log

@app_commands.command(name="joke", description="Get a random joke.")
async def joke(interaction : discord.Interaction):
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
            await interaction.response.send_message(res["joke"])
        else:
            if res["type"] == "twopart":
                await interaction.response.send_message(f"{res['setup']}\n||{res['delivery']}||")
            else:
                await interaction.response.send_message(res["joke"])
    except Exception as e:
        await interaction.response.send_message("An error occurred while fetching a joke. Please check the logs for more details.")
        log.error(f"An error occurred while fetching a joke: {e}")

async def setup(bot):
    bot.add_command(joke)