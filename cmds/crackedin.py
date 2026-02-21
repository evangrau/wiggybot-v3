from discord.ext import commands
from classes.dbconnection import DBConnection
from loguru import logger as log
from settings import MODE

@commands.hybrid_command()
async def crackedin(ctx):
    """Opts you in to daily cracked."""

    log.info("Running crackedin command...")

    try:
        # getting access to the database
        db = DBConnection()

        # check to make sure they aren't already in the db
        records = db.get_all_records(f"cracked_table_{MODE}")
        
        for _, r in records.iterrows():
            if r['fields.discord_id'] == str(ctx.author.id):
                await ctx.send(f"<@{ctx.author.id}>, you have already opted in.")
                log.warning(f"{ctx.author.name} ({ctx.author.id}) has already opted in to crackedin. Returning without adding to database.")
                return

        # updating the database
        record = {"discord_id": f"{ctx.author.id}", "username": f"{ctx.author.name}", "cracked": 0, "bad": 0}
        db.create_record(f"cracked_table_{MODE}", record)
        log.info(f"{ctx.author.name} ({ctx.author.id}) has been added to the cracked_table_{MODE} in Airtable with record: {record}.")

        await ctx.send(f"<@{ctx.author.id}>, you have opted in to be cracked... or bad.")
    except Exception as e:
        await ctx.send("An error occurred while running the crackedin command. Please check the logs for more details.")
        log.error(f"An error occurred while running crackedin command: {e}")


async def setup(bot):
    bot.add_command(crackedin)