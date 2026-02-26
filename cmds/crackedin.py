from settings import ADMIN_IDS
from discord.ext import commands
from db import database as db
from loguru import logger as log

WIGGY_ID = ADMIN_IDS[0]

@commands.hybrid_command(name="crackedin", description="Opts you in to daily cracked.")
async def crackedin(ctx : commands.Context):
    """Opts you in to daily cracked."""

    log.info("Running crackedin command...")

    try:
        # check to make sure they aren't already in the db
        records = db.get_all_cracked_records()
        
        for _, r in records.iterrows():
            if r['discord_id'] == ctx.author.id:
                if r['visible'] == False:
                    db.update_record(f'cracked', r['discord_id'], {"visible": True})
                    await ctx.send(f"<@{ctx.author.id}>, you have opted back in to being cracked or bad.")
                    log.info(f"{ctx.author.name} ({ctx.author.id}) has been updated in the cracked table with record: {{'visible': True}}.")
                    return
                else:
                    await ctx.send(f"<@{ctx.author.id}>, you have already opted in.")
                    log.warning(f"{ctx.author.name} ({ctx.author.id}) has already opted in to crackedin. Returning without adding to database.")
                    return

        # updating the database
        record = {"discord_id": f"{ctx.author.id}", "username": f"{ctx.author.name}", "cracked": 0, "bad": 0, "visible": True}
        db.create_record("cracked", record)
        log.info(f"{ctx.author.name} ({ctx.author.id}) has been added to the cracked table with record: {record}.")
        await ctx.send(f"<@{ctx.author.id}>, you have opted in to be cracked... or bad.")
    except Exception as e:
        await ctx.send(f"An error occurred while running the crackedin command. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")
        log.error(f"An error occurred while running crackedin command: {e}")


async def setup(bot):
    bot.add_command(crackedin)