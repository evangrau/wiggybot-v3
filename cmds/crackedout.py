from discord.ext import commands
from settings import ADMIN_IDS
from db import database as db
from loguru import logger as log

WIGGY_ID = ADMIN_IDS[0]

@commands.hybrid_command(name="crackedout", description="Opts you out of daily cracked.")
async def crackedout(ctx : commands.Context):
    """Opts you out of daily cracked."""

    log.info("Running crackedout command...")

    try:
        # check to make sure they are in the db
        records = db.get_all_cracked_records()
        
        for _, r in records.iterrows():
            if r['discord_id'] == ctx.author.id:
                if r['visible'] == True:
                    db.update_record(f'cracked', r['discord_id'], {"visible": False})
                    await ctx.send(f"<@{ctx.author.id}>, you have opted out of being cracked or bad. Don't worry, your data is saved and you can opt back in at any time with the `crackedin` command.")
                    log.info(f"{ctx.author.name} ({ctx.author.id}) has been updated in the cracked table with record: {{'visible': False}}.")
                    return
                else:
                    await ctx.send(f"<@{ctx.author.id}>, you have already opted out.")
                    log.warning(f"{ctx.author.name} ({ctx.author.id}) has already opted out of crackedout. Returning without updating the database.")
                    return

        await ctx.send(f"<@{ctx.author.id}>, you are not currently opted in.")
        log.warning(f"{ctx.author.name} ({ctx.author.id}) attempted to use crackedout command but was not found in the database.")
    except Exception as e:
        await ctx.send(f"An error occurred while running the crackedout command. Please check the logs for more details. <@{WIGGY_ID}> fix your bot.")
        log.error(f"An error occurred while running crackedout command: {e}")

async def setup(bot):
    bot.add_command(crackedout)