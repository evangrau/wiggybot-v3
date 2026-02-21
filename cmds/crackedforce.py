from discord.ext import commands
from utils import get_cracked
from loguru import logger as log
from settings import ADMIN_IDS

@commands.command(hidden=True)
async def crackedforce(ctx):
    """Forces cracked if the bot doesn't go off."""

    log.info("Running crackedforce command...")

    if ctx.author.id not in ADMIN_IDS:
        await ctx.send("You are are not authorized to use this command.")
        log.warning(f"{ctx.author.name} ({ctx.author.id}) attempted to use crackedforce command. Returning without executing.")
        return
    
    await get_cracked(ctx)
    

async def setup(bot):
    bot.add_command(crackedforce)