from discord.ext import commands
from classes.dbconnection import DBConnection
from loguru import logger as log
from settings import MODE

@commands.hybrid_command()
async def crackedout(ctx):
    """Opts you out of daily cracked."""

    log.info("Running crackedout command...")

    try:
        # getting access to the database
        db = DBConnection()

        # check to make sure they are in the db
        records = db.get_all_records("cracked_table_{MODE}")
        
        for _, r in records.iterrows():
            if r['fields.discord_id'] == str(ctx.author.id):
                db.delete_record(f'cracked_table_{MODE}', r['id'])
                await ctx.send(f"<@{ctx.author.id}>, you have opted out of being cracked or bad.")
                log.info(f"{ctx.author.name} ({ctx.author.id}) has been removed from the cracked_table_{MODE} in Airtable.")
                return

        await ctx.send(f"<@{ctx.author.id}>, you are not currently opted in.")
        log.warning(f"{ctx.author.name} ({ctx.author.id}) attempted to use crackedout command but was not found in the database.")
    except Exception as e:
        await ctx.send("An error occurred while running the crackedout command. Please check the logs for more details.")
        log.error(f"An error occurred while running crackedout command: {e}")

async def setup(bot):
    bot.add_command(crackedout)