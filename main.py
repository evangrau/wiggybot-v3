import discord
import settings
from argparse import ArgumentParser
from discord.ext import commands
from loguru import logger as log

def main(args):

    log.info(f"Starting wiggy Bot in {args.mode} mode...")

    # Set a variable in settings to indicate the mode
    settings.MODE = args.mode

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    activity = discord.Game(name=f"{settings.COMMAND_PREFIX}help")
    
    bot = commands.AutoShardedBot(command_prefix=settings.COMMAND_PREFIX, intents=intents, activity=activity)
    
    @bot.event
    async def on_ready():
        log.debug(f"User: {bot.user} (ID: {bot.user.id}, Shards: {bot.shard_count})")
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

    @bot.hybrid_command(hidden=True)
    @commands.is_owner()
    async def load(ctx, cog: str):
        log.debug(f"Attempting to load cog: {cog}")
        await bot.load_extension(f"cogs.{cog.lower()}")
    
    @bot.hybrid_command(hidden=True)
    @commands.is_owner()
    async def unload(ctx, cog: str):
        log.debug(f"Attempting to unload cog: {cog}")
        await bot.unload_extension(f"cogs.{cog.lower()}")

    @bot.hybrid_command(hidden=True)
    @commands.is_owner()
    async def reload(ctx, cog: str):
        log.debug(f"Attempting to reload cog: {cog}")
        await bot.reload_extension(f"cogs.{cog.lower()}")

    @bot.hybrid_command()
    @commands.is_owner()
    async def shardinfo(ctx):
        sid = ctx.guild.shard_id
        shard = bot.get_shard(sid)
        await ctx.send(f"Guild shard: {sid} | shard latency: {shard.latency*1000:.0f}ms")
    
    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":

    parser = ArgumentParser(description="Run the wiggy bot.")

    parser.add_argument(
        "-m", "--mode",
        choices=["dev", "prod"],
        default="prod",
        help="Set the mode for the bot (default: prod)",
        required=True
    )

    args = parser.parse_args()

    main(args)
