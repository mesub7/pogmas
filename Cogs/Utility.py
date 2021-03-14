import discord
from discord.ext import commands
import time
from datetime import datetime
import Cogs.Checks as k
import asyncio
import aiosqlite

class Utility(commands.Cog):
    """The Utility cog. Provides helpful information and functions."""

    def __init__(self, bot):
        self.bot = bot
        self.bot.todo = []

    @commands.command(desription='Pings the bot.', help='Pings the bot.')
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send('Ping...')
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content='Pong!\nCommand processing: `{:.2f}ms`\nDiscord latency: `{:.2f}ms`'.format(duration, self.bot.latency*1000))

    @commands.command(description='Some info about the bot.', help='Some infomation about the bot.')
    async def about(self, ctx):
        user = self.bot.get_user(414530505585721357)
        embed = discord.Embed(title=str(self.bot.user.name), colour=discord.Colour.blue(), description='A simple discord bot for Transport Dash (and qualifying servers), built and maintained by mesub#0556.')
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_footer(text='mesub#0556', icon_url=user.avatar_url)
        embed.add_field(name='About', value='This is just a simple bot to make some tasks in Transport Dash (and qualifying servers) a little easier. Don\'t expect too much functionality outside it 😄.')
        embed.add_field(name='Source code', value='If you want to play around with the bot or run an instance of it, then the code can be found [here](https://github.com/mesub7/pogmas) and an invite [here](https://discord.com/api/oauth2/authorize?client_id=746370972528934953&permissions=67152896&scope=bot)')
        await ctx.send(embed=embed)

    @commands.command(description='See how long the bot has been online for!', help='Checks bot uptime.')
    async def uptime(self, ctx):
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f'I have been up for: {days}d, {hours}h, {minutes}m, and {seconds}s')

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(769941819344814140)
        if self.bot.user.mentioned_in(message):
            embed = discord.Embed(title='I was mentioned!', colour=discord.Colour.purple(), description=f'I was mentioned by `{message.author}` in <#{message.channel.id}> in the server `{message.guild}` . \n Content: \'{message.content}\' \n Jumplink: {message.jump_url}.')
            await channel.send(embed=embed)

    @commands.command(name='check', description='Checks if you are part of an internal permission group to run elevated commands'\
    , help='Are you elite?')
    async def checker(self, ctx, user:discord.Member=None):
        msg = await ctx.send('Checking...')
        if user:
            ctx.author=user
        await asyncio.sleep(5)
        if await k.lvl5(ctx):
            await msg.edit(content=f'{ctx.author.name} is in `level 5`.')
        elif await k.lvl4(ctx):
            await msg.edit(content=f'{ctx.author.name} is in `level 4`.')
        elif await k.lvl3(ctx):
            await msg.edit(content=f'{ctx.author.name} is in: `level 3`.')
        elif await k.lvl2(ctx):
            await msg.edit(content=f'{ctx.author.name} is in `level 2`.')
        else:
            await msg.edit(content=f'{ctx.author.name} is in `level 1` (No level).')

    async def db_to_embed(self):
        list = []
        self.bot.db.row_factory = aiosqlite.Row
        x = await self.bot.db.execute("SELECT * FROM todo")
        row = await x.fetchall()
        for rows in row:
            list.append(f"{str(rows['id']) + '.  ' + rows['todo']}")
        return None if not list else list

    @commands.check(k.lvl5)
    @commands.group(help='Make my life easier.', aliases=['td'], invoke_without_command=True)
    async def todo(self, ctx):
        x = '\n'
        list = await self.db_to_embed()
        if list is not None:
            formatted_tasks = x.join(str(item) for item in list)
        else:
            formatted_tasks = 'No tasks! Very productive.'
        embed = discord.Embed(title=f'Todo - {self.bot.get_user(self.bot.owner_id)}',
        description=f'{formatted_tasks}', colour=discord.Colour.blue())
        await ctx.send(embed=embed)

    @todo.command(help='Add something to do.', aliases=['a'])
    async def add(self, ctx, *chores):
        async with ctx.channel.typing():
            for chore in chores:
                    await self.bot.db.execute('INSERT INTO todo(todo) VALUES(?);', (chore,))
            await self.bot.db.commit()
            await ctx.send('Tasks added!')

    @todo.command(help='Remove a completed (or cancelled) task.', aliases=['r'])
    async def remove(self, ctx, *ids):
        async with ctx.channel.typing():
            if 'clear' or 'all' in ids:
                await self.bot.db.execute('DELETE FROM todo')
                await ctx.send('Removed all tasks!')
                await self.bot.db.commit()
                return
            else:
                failed = []
                for id in ids:
                    try:
                        await self.bot.db.execute('DELETE FROM todo WHERE id=?;', (id,))
                    except Exception as e:
                        failed.append(word)
                        await self.bot.db.commit()
                    if not failed:
                        await ctx.send('Tasks removed!')
                    else:
                        x = '\n'
                        await ctx.send(f'Some tasks were not removed...\n```\n{x.join(str(f) for f in failed)}\n```')

def setup(bot):
    bot.add_cog(Utility(bot))
