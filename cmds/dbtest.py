from discord.ext import commands
from settings import ADMIN_IDS
from loguru import logger as log
from db import database as db

WIGGY_ID = ADMIN_IDS[0]

@commands.hybrid_command(name="dbtest", description="Test command to check if database connection is working.")
async def dbtest(ctx : commands.Context):
    """Test command to check if database connection is working."""

    log.info("Running dbtest command...")

    try:
        records = db.get_all_cracked_records()
        # records = await db.get_random_quote()
        if not records.empty:
            await ctx.send(f"Successfully retrieved {len(records)} records from the database!")
            log.debug(f"Records: {records}")
        else:
            await ctx.send(f"Failed to retrieve records from the database. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")
            log.warning("No records retrieved from the database.")
    except Exception as e:
        await ctx.send(f"An error occurred while connecting to the database. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")
        log.error(f"An error occurred while connecting to the database: {e}")

async def setup(bot):
    bot.add_command(dbtest)