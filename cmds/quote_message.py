import discord
from discord import app_commands
from loguru import logger as log
from db import database as db

@app_commands.context_menu(name="Quote Message")
async def quote_message(interaction: discord.Interaction, message: discord.Message):
    """Context menu command to quote a message."""
        
    log.info("Running quote_message command...")

    quote = message.content
    author = message.author

    try:
        db.create_record('quotes', author.id, {'quote': quote, 'author': author.id})
        log.info(f"Inserted quote into the database: {quote} - {author.name} ({author.id})")
        await interaction.response.send_message(f"Quote added: {quote} - {author.mention}")
    except Exception as e:
        log.error(f"An error occurred while inserting quote into the database: {e}")
        await interaction.response.send_message("An error occurred while adding the quote. Please tell wiggy to check the logs for more details.", ephemeral=True)

async def setup(bot):
    bot.tree.add_command(quote_message)