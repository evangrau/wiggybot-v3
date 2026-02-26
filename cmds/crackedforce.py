import random
import discord
from discord import app_commands
from db import database as db
from loguru import logger as log
from settings import ADMIN_IDS

@app_commands.command(name="crackedforce", description="Forces cracked if the bot doesn't go off.")
async def crackedforce(interaction : discord.Interaction):
    """Forces cracked if the bot doesn't go off."""

    log.info("Running crackedforce command...")

    if interaction.user.id not in ADMIN_IDS:
        await interaction.response.send_message("You are are not authorized to use this command.")
        log.warning(f"{interaction.user.name} ({interaction.user.id}) attempted to use crackedforce command. Returning without executing.")
        return
    
    try:
        # getting access to the database
        records = db.get_all_cracked_records()

        members = []

        if not records.empty:
            for _, r in records.iterrows():
                if r['visible'] == True:
                    members.append({"discord_id": r['discord_id'], "username": r['username'], "cracked": r['cracked'], "bad": r['bad'], "ratio": r['ratio']})
        else:
            raise ValueError(f"No records found in the cracked table.")

        ratios = [r["ratio"] for r in members]
        min_ratio = min(ratios)
        weights = [1 / (ratio - min_ratio + 1) for ratio in ratios]
        log.debug(f"Members: {members}, Weights: {weights}")
        m = random.choices(members, weights=weights, k=1)[0]

        rand = random.randint(0, 99)

        if (rand < 5):
            # bad
            await interaction.response.send_message(f"<@{m['discord_id']}>, you're bad.")
            await db.update_record('cracked', m['discord_id'], {"bad": m['bad'] + 1})
            log.info(f"Cracked command ran and {m['username']} was bad: {{'bad': {m['bad'] + 1}}}")
        else:
            # cracked
            await interaction.response.send_message(f"<@{m['discord_id']}>, you're cracked.")
            await db.update_record('cracked', m['discord_id'], {"cracked": m['cracked'] + 1})
            log.info(f"Cracked command ran and {m['username']} was cracked: {{'cracked': {m['cracked'] + 1}}}")
    except Exception as e:
        await interaction.response.send_message("An error occurred while running the cracked command. Please check the logs for more details.")
        log.error(f"An error occurred while running cracked command: {e}")
    

async def setup(bot):
    bot.add_command(crackedforce)