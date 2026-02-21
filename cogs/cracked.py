import datetime
import settings
from discord.ext import commands, tasks
from utils import get_cracked
from loguru import logger as log

CHANNEL_ID = settings.GENERAL_CHANNEL_ID

CST = datetime.timezone(datetime.timedelta(hours=-6))
TIME = datetime.time(hour=12, tzinfo=CST)

class Cracked(commands.Cog):

    def __init__(self, bot):
        self.get_daily_cracked.start()
        self.bot = bot
        self.channel = self.bot.get_channel(CHANNEL_ID)

    def cog_unload(self):
        self.get_daily_cracked.cancel()

    # @tasks.loop(seconds=5.0)
    @tasks.loop(time=TIME)
    async def get_daily_cracked(self):
        log.info("Running daily cracked task...")
        await get_cracked(self.channel)

async def setup(bot):
    await bot.add_cog(Cracked(bot))