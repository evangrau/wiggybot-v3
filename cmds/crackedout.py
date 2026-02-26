import discord
from discord import app_commands
from db import database as db
from loguru import logger as log
from settings import MODE

@app_commands.command(name="crackedout", description="Opts you out of daily cracked.")
async def crackedout(interaction : discord.Interaction):
    """Opts you out of daily cracked."""

    log.info("Running crackedout command...")

    try:
        # check to make sure they are in the db
        records = db.get_all_cracked_records()
        
        for _, r in records.iterrows():
            if r['discord_id'] == interaction.user.id:
                if r['visible'] == True:
                    db.update_record(f'cracked', r['discord_id'], {"visible": False})
                    await interaction.response.send_message(f"<@{interaction.user.id}>, you have opted out of being cracked or bad. Don't worry, your data is saved and you can opt back in at any time with the `crackedin` command.")
                    log.info(f"{interaction.user.name} ({interaction.user.id}) has been updated in the cracked table with record: {{'visible': False}}.")
                    return
                else:
                    await interaction.response.send_message(f"<@{interaction.user.id}>, you have already opted out.")
                    log.warning(f"{interaction.user.name} ({interaction.user.id}) has already opted out of crackedout. Returning without updating the database.")
                    return

        await interaction.response.send_message(f"<@{interaction.user.id}>, you are not currently opted in.")
        log.warning(f"{interaction.user.name} ({interaction.user.id}) attempted to use crackedout command but was not found in the database.")
    except Exception as e:
        await interaction.response.send_message("An error occurred while running the crackedout command. Please check the logs for more details.")
        log.error(f"An error occurred while running crackedout command: {e}")

async def setup(bot):
    bot.add_command(crackedout)