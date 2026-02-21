import discord
from discord.ext import commands
import random
import settings

CLIPS = settings.CLIPS_CHANNEL_ID

class MessageResponse(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg : discord.Message):

        amogus_responses = [
            "https://tenor.com/view/among-us-gif-21088542",
            "https://tenor.com/view/sushichaeng-among-us-among-us-meme-shocked-confused-gif-22454610",
            "https://tenor.com/view/among-us-dance-dance-among-us-purple-sus-gif-18888988",
            "AMOGUS ⛔",
            "sus",
            "sussy",
            "AMONG US?!?! 😱"
            'amo gus ❤️',
            'https://tenor.com/bCyCo.gif',
            'https://tenor.com/bLDhX.gif',
            'https://tenor.com/bN3rW.gif'
        ]

        amogus_options = [
            "among us",
            "amogus",
            "mogus",
            "amongus"
        ]

        your_mom_responses = [
            'your mother 😏',
            'ur mom',
            'ur mum lol',
            'thine mother 🧐',
            'your mom 😎',
            'your\'re mother 🤓',
            'thine female parental figure 🧐'
        ]

        your_mom_triggers = [
            'i am doing',
            'we are doing',
            'you are doing',
            'am i doing',
            'are we doing',
            'are you doing',
            'i will do',
            'we will do',
            'you will do',
            'will i do',
            'will we do',
            'will you do'
        ]

        wordle = [
            "bruh",
            "you're bad lol",
            "oof",
            "dang...",
            "How lmao This one was literally so easy",
            "pain",
            "kinda sus ngl",
            "what are you doing bruh",
            "guess you didn't pop off irl 😔"
        ]

        mentionResponses = [
            "Hello Mario",
            "why you mention me",
            "🗿",
            "bru",
            "bruh"
        ]

        for op in amogus_options:
            if op in msg.content.lower():
                rand = random.choice(amogus_responses)
                await msg.channel.send(rand)

        for t in your_mom_triggers:
            if t in msg.content.lower():
                rand = random.choice(your_mom_responses)
                await msg.reply(rand)

        if 'x/6' in msg.content.lower():
            rand = random.choice(wordle)
            await msg.reply(rand)

        if str(self.bot.user.id) in msg.mentions and msg.author.id != self.bot.user.id:
            rand = random.choice(mentionResponses)
            await msg.reply(rand)

        if ' ayo ' in msg.content.lower():
            await msg.channel.send("ayooo? 🤨")

        if 'hello there' in msg.content.lower():
            await msg.reply("General Kenobi!")

        if 'kanye' in msg.content.lower():
            await msg.reply("ye da 🐐 no 🧢")

        if msg.channel.id == CLIPS:
            if 'https://medal.tv' in msg.content.lower() or 'https://www.gifyourgame.com' in msg.content.lower():
                await msg.add_reaction("👀")

        

async def setup(bot):
    await bot.add_cog(MessageResponse(bot))