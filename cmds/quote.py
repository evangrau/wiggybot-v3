from discord.ext import commands
from settings import ADMIN_IDS
from loguru import logger as log
from db import database as db

WIGGY_ID = ADMIN_IDS[0]

@commands.hybrid_command(name="quote", description="Get a random quote.")
async def quote(ctx: commands.Context):
    """Get a random quote from the database."""

    log.info("Running quote command...")

    try:
        quote_record = db.get_random_quote()
        if not quote_record.empty:
            log.debug(quote_record)
            log.info(f"Successfully retrieved quote from the database: {quote_record.iloc[0]['quote']} - {quote_record.iloc[0]['author']}")
            await ctx.send(f"{quote_record.iloc[0]['quote']} - <@{quote_record.iloc[0]['author']}>")
        else:
            await ctx.send(f"Failed to retrieve a quote from the database. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")
            log.warning("No quote retrieved from the database.")
    except Exception as e:
        await ctx.send(f"An error occurred while running the quote command. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")
        log.error(f"An error occurred while running the quote command: {e}")

async def setup(bot):
    bot.add_command(quote)