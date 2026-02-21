import random
import discord
import settings
from discord.ext import commands
from loguru import logger as log

def main():

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    activity = discord.Game(name=f"Use {settings.COMMAND_PREFIX}help for commands!")
    
    bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX, intents=intents, activity=activity)
    
    @bot.event
    async def on_ready():
        log.debug(f"User: {bot.user} (ID: {bot.user.id})")
        log.info("wiggy Bot is Online!")

        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                log.debug(f"Attempting to load command: {cmd_file.name[:-3]}")
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                log.debug(f"Attempting to load cog: {cog_file.name[:-3]}")
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)


    @bot.tree.context_menu(name="Show join date")
    async def get_join_date(interaction : discord.Interaction, member : discord.Member):
        await interaction.response.send_message(f"{member.name} joined on {discord.utils.format_dt(member.joined_at)}", ephemeral=True)

    @bot.command(hidden=True)
    @commands.is_owner()
    async def load(ctx, cog: str):
        log.debug(f"Attempting to load cog: {cog}")
        await bot.load_extension(f"cogs.{cog.lower()}")
    
    @bot.command(hidden=True)
    @commands.is_owner()
    async def unload(ctx, cog: str):
        log.debug(f"Attempting to unload cog: {cog}")
        await bot.unload_extension(f"cogs.{cog.lower()}")

    @bot.command(hidden=True)
    @commands.is_owner()
    async def reload(ctx, cog: str):
        log.debug(f"Attempting to reload cog: {cog}")
        await bot.reload_extension(f"cogs.{cog.lower()}")
    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    main()
