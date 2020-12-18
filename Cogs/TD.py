import discord
from discord.ext import commands, tasks
import asyncio
import datetime

class TD(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.auto_brexit.start()
        self.quest_enq.start()
        self.quest_pick.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = 703665588244971582
        emoji = '\N{THUMBS UP SIGN}'
        emoji1 = '\N{THUMBS DOWN SIGN}'
        emoji2 = 'a:siren:789554809006325760'
        role = message.guild.get_role(703230475472207924)
        if channel == int(message.channel.id):
            await message.add_reaction(emoji)
            await asyncio.sleep(1)
            await message.add_reaction(emoji1)
        if role.mention in message.content.lower():
            await message.channel.send("<a:siren:789554809006325760> **Staff on duty have been notified, please stand by.** <a:siren:789554809006325760>")
            await message.add_reaction(emoji2)
            await role.edit(mentionable=False, reason="Staff on duty role mentioned.")
            await asyncio.sleep(120)
            await role.edit(mentionable=True, reason="Cooldown reached - Role can be mentioned again.")

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

    @tasks.loop(hours=24)
    async def quest_enq(self):
        dt = datetime.datetime
        now = dt.now()
        channel = self.bot.get_channel(720709557445460028)
        if now.weekday() == 5:
            await channel.send("<@414530505585721357> Don't forget to ask about questioners!")

    @quest_enq.before_loop
    async def before_qe(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=24)
    async def quest_pick(self):
        dt = datetime.datetime
        now = dt.now()
        channel = self.bot.get_channel(720709557445460028)
        if now.weekday() == 6:
            await channel.send("<@414530505585721357> Don't forget to pick a questioner!")

    @quest_pick.before_loop
    async def before_pick(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(TD(bot))
