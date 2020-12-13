import discord
from discord.ext import commands, tasks
import asyncio
import datetime

class TD(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = 703665588244971582
        emoji = '\N{THUMBS UP SIGN}'
        emoji1 = '\N{THUMBS DOWN SIGN}'
        if channel == int(message.channel.id):
            await message.add_reaction(emoji)
            await asyncio.sleep(1)
            await message.add_reaction(emoji1)

    @tasks.loop(hours=24)
    async def auto_brexit(self):
        channel = self.bot.get_channel(395956678412992523)
        dt  = datetime.datetime
        now = dt.now()
        cd=dt(year=2021, month=1,day=1) - dt(year=now.year, month=now.month, day=now.day)
        await channel.send(f'There are `'+str(cd)[:str(cd).find(",")]+'` until <:BR:772541846357278791><:EX:772541846358196254><:IT:756911540728496220>')

    @auto_brexit.before_loop
    async def before_brexit(self):
        await self.bot.wait_until_ready()

    auto_brexit.start()
def setup(bot):
    bot.add_cog(TD(bot))
