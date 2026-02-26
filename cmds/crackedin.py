import discord
from discord import app_commands
from db import database as db
from loguru import logger as log
from settings import MODE

@app_commands.command(name="crackedin", description="Opts you in to daily cracked.")
async def crackedin(interaction : discord.Interaction):
    """Opts you in to daily cracked."""

    log.info("Running crackedin command...")

    try:
        # check to make sure they aren't already in the db
        records = db.get_all_cracked_records()
        
        for _, r in records.iterrows():
            if r['discord_id'] == interaction.user.id:
                if r['visible'] == False:
                    db.update_record(f'cracked', r['discord_id'], {"visible": True})
                    await interaction.response.send_message(f"<@{interaction.user.id}>, you have opted back in to being cracked or bad.")
                    log.info(f"{interaction.user.name} ({interaction.user.id}) has been updated in the cracked table with record: {{'visible': True}}.")
                    return
                else:
                    await interaction.response.send_message(f"<@{interaction.user.id}>, you have already opted in.")
                    log.warning(f"{interaction.user.name} ({interaction.user.id}) has already opted in to crackedin. Returning without adding to database.")
                    return

        # updating the database
        record = {"discord_id": f"{interaction.user.id}", "username": f"{interaction.user.name}", "cracked": 0, "bad": 0, "visible": True}
        db.create_record("cracked", record)
        log.info(f"{interaction.user.name} ({interaction.user.id}) has been added to the cracked table with record: {record}.")
        await interaction.response.send_message(f"<@{interaction.user.id}>, you have opted in to be cracked... or bad.")
    except Exception as e:
        await interaction.response.send_message("An error occurred while running the crackedin command. Please check the logs for more details.")
        log.error(f"An error occurred while running crackedin command: {e}")


async def setup(bot):
    bot.add_command(crackedin)