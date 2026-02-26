import discord
from discord import app_commands
from discord import Embed, Color
from db import database as db
from loguru import logger as log
from settings import MODE

@app_commands.command(name="crackedlb", description="Gets the cracked/bad leaderboard.")
async def crackedlb(interaction : discord.Interaction):
    """Gets the cracked/bad leaderboard."""

    log.info("Running crackedlb command...")

    try:
        records = db.get_all_cracked_records()
        members = []

        if not records.empty:
            for _, r in records.iterrows():
                if r['visible'] == True:
                    members.append([r['discord_id'], r['cracked'], r['bad']])
        else:
            raise ValueError(f"No records found in the cracked table.")
        
        # creating the embed
        names = ""
        cracked = ""
        bad = ""

        for i in range(len(members)):
            names += f"{i}. <@{members[i][0]}>\n"
            cracked += f"{members[i][1]}\n"
            bad += f"{members[i][2]}\n"

        embed = Embed(
            color= Color.dark_purple(),
            title="wiggy Bot Cracked Leaderboard",
            description="The wiggy Bot cracked/bad leaderboard"
        )

        embed.add_field(name="Name", value=names)
        embed.add_field(name="Cracked", value=cracked)
        embed.add_field(name="Bad", value=bad)

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await interaction.response.send_message("An error occurred while running the crackedlb command. Please check the logs for more details.")
        log.error(f"An error occurred while running crackedlb command: {e}")

async def setup(bot):
    bot.add_command(crackedlb)