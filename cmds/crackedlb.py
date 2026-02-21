from discord.ext import commands
from discord import Embed, Color
from classes.dbconnection import DBConnection
from loguru import logger as log
from settings import MODE

@commands.hybrid_command()
async def crackedlb(ctx):
    """Gets the cracked/bad leaderboard."""

    log.info("Running crackedlb command...")

    try:
        # getting access to the database
        db = DBConnection()

        records = db.get_all_records(f"cracked_table_{MODE}", sort_by=["cracked:bad"])
        members = []

        if not records.empty:
            for _, r in records.iterrows():
                if r['fields.visible_bool'] == True:
                    members.append([r['fields.discord_id'], r['fields.cracked'], r['fields.bad'], r['fields.cracked:bad']])
        else:
            raise ValueError(f"No records found in the 'cracked_table_{MODE}' Airtable table.")
        
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

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("An error occurred while running the crackedlb command. Please check the logs for more details.")
        log.error(f"An error occurred while running crackedlb command: {e}")

async def setup(bot):
    bot.add_command(crackedlb)