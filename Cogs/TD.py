import discord
from discord.ext import commands
import asyncio

class TD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = 703665588244971582
        emoji = '\N{THUMBS UP SIGN}'
        emoji1 = '\N{THUMBS DOWN SIGN}'
        if channel == int(message.channel.id):
            await message.add_reaction(emoji)
            asyncio.sleep(1)
            await message.add_reaction(emoji1)
        await self.bot.process_commands(message)
def setup(bot):
    bot.add_cog(TD(bot))
