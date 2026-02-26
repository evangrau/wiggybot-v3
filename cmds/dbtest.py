import discord
from discord import app_commands
from loguru import logger as log
from db import database as db

@app_commands.command(name="dbtest", description="Test command to check if database connection is working.")
async def dbtest(interaction : discord.Interaction):
    """Test command to check if database connection is working."""

    log.info("Running dbtest command...")

    try:
        records = db.get_all_cracked_records()
        # records = await db.get_random_quote()
        if not records.empty:
            await interaction.response.send_message(f"Successfully retrieved {len(records)} records from the database!")
            log.debug(f"Records: {records}")
        else:
            await interaction.response.send_message("Failed to retrieve records from the database. Please check the logs for more details.")
            log.warning("No records retrieved from the database.")
    except Exception as e:
        await interaction.response.send_message("An error occurred while connecting to the database. Please check the logs for more details.")
        log.error(f"An error occurred while connecting to the database: {e}")

async def setup(bot):
    bot.add_command(dbtest)