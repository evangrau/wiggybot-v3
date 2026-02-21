from discord.ext import commands
from classes.dbconnection import DBConnection
from loguru import logger as log

@commands.hybrid_command(hidden=True)
@commands.is_owner()
async def airtable_test(ctx):
    """Test command to check if Airtable connection is working."""

    log.info("Running airtable_test command...")

    try:
        db = DBConnection()
        records = db.get_all_records("cracked_table")
        if not records.empty:
            await ctx.send(f"Successfully retrieved {len(records)} records from Airtable!")
            log.info(f"Successfully retrieved {len(records)} records from Airtable!")
            log.debug(f"Records: {records}")
        else:
            await ctx.send("Failed to retrieve records from Airtable. Please check the logs for more details.")
            log.warning("No records retrieved from Airtable.")
    except Exception as e:
        await ctx.send("An error occurred while connecting to Airtable. Please check the logs for more details.")
        log.error(f"An error occurred while connecting to Airtable: {e}")

async def setup(bot):
    bot.add_command(airtable_test)