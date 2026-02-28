import discord
from discord.ext import commands
from settings import ADMIN_IDS
from loguru import logger as log
from db import database as db

WIGGY_ID = ADMIN_IDS[0]

@commands.hybrid_command(name="quote_that", description="Quote something.")
async def quote_that(ctx: commands.Context, quote: str, author: discord.User):
    """Quotes a message with the provided quote and author."""

    log.info("Running quote_that command...")

    try:
        # Insert the quote into the database
        db.create_record('quotes', author.id, {'quote': quote, 'author': author.id})
        log.info(f"Inserted quote into the database: {quote} - {author.name} ({author.id})")
        await ctx.send(f"Quote added: {quote} - {author.mention}")
    except Exception as e:
        log.error(f"An error occurred while inserting quote into the database: {e}")
        await ctx.send(f"An error occurred while adding the quote. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")

async def setup(bot):
    bot.add_command(quote_that)