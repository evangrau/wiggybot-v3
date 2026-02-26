import datetime
import settings
import random
from discord.ext import commands, tasks
from db import database as db
from discord.ext import commands, tasks
from loguru import logger as log

CHANNEL_ID = settings.GENERAL_CHANNEL_ID

CST = datetime.timezone(datetime.timedelta(hours=-6))
TIME = datetime.time(hour=12, tzinfo=CST)

class Cracked(commands.Cog):

    def __init__(self, bot : commands.Bot):
        self.get_daily_cracked.start()
        self.bot = bot
        self.channel = self.bot.get_channel(CHANNEL_ID)

    def cog_unload(self):
        self.get_daily_cracked.cancel()

    # @tasks.loop(seconds=5.0)
    @tasks.loop(time=TIME)
    async def get_daily_cracked(self):
        log.info("Running daily cracked task...")
        
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
                await self.channel.send(f"<@{m['discord_id']}>, you're bad.")
                await db.update_record('cracked', m['discord_id'], {"bad": m['bad'] + 1})
                log.info(f"Cracked command ran and {m['username']} was bad: {{'bad': {m['bad'] + 1}}}")
            else:
                # cracked
                await self.channel.send(f"<@{m['discord_id']}>, you're cracked.")
                await db.update_record('cracked', m['discord_id'], {"cracked": m['cracked'] + 1})
                log.info(f"Cracked command ran and {m['username']} was cracked: {{'cracked': {m['cracked'] + 1}}}")
        except Exception as e:
            await self.channel.send("An error occurred while running the cracked command. Please check the logs for more details.")
            log.error(f"An error occurred while running cracked command: {e}")

async def setup(bot):
    await bot.add_cog(Cracked(bot))