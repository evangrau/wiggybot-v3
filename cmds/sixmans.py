from discord.ext import commands
from loguru import logger as log

@commands.hybrid_command(name="6mans")
async def sixmans(ctx):
    """6mans is coming soon!"""

    log.info("Running 6mans command...")

    await ctx.send("6mans is coming soon!")