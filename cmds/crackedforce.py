import random
from discord.ext import commands
from db import database as db
from loguru import logger as log
from settings import ADMIN_IDS

@commands.hybrid_command(name="crackedforce", description="Forces cracked if the bot doesn't go off.")
async def crackedforce(ctx : commands.Context):
    """Forces cracked if the bot doesn't go off."""

    log.info("Running crackedforce command...")

    if ctx.author.id not in ADMIN_IDS:
        await ctx.send("You are are not authorized to use this command.")
        log.warning(f"{ctx.author.name} ({ctx.author.id}) attempted to use crackedforce command. Returning without executing.")
        return
    
    try:
        # getting access to the database
        records = db.get_all_cracked_records()

        members = []

        if not records.empty:
            for _, r in records.iterrows():
                if r['visible'] == True:
                    members.append({"discord_id": r['discord_id'], "username": r['username'], "cracked_count": r['cracked_count'], "bad_count": r['bad_count'], "ratio": r['ratio']})
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
            await ctx.send(f"<@{m['discord_id']}>, you're bad.")
            await db.update_record('cracked', m['discord_id'], {"bad_count": m['bad_count'] + 1})
            log.info(f"Cracked command ran and {m['username']} was bad: {{'bad_count': {m['bad_count'] + 1}}}")
        else:
            # cracked
            await ctx.send(f"<@{m['discord_id']}>, you're cracked.")
            await db.update_record('cracked', m['discord_id'], {"cracked_count": m['cracked_count'] + 1})
            log.info(f"Cracked command ran and {m['username']} was cracked: {{'cracked_count': {m['cracked_count'] + 1}}}")
    except Exception as e:
        await ctx.send("An error occurred while running the cracked command. Please check the logs for more details.")
        log.error(f"An error occurred while running cracked command: {e}")
    

async def setup(bot):
    bot.add_command(crackedforce)