import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import Cogs.Checks as k
import aiosqlite


class TD(commands.Cog):
    """The Transport Dash Cog. Contains functions exclusive to Transport Dash"""

    def __init__(self, bot):
        self.bot = bot
        self.quest_enq.start()
        self.quest_pick.start()
        self.questioner_reminder.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.guild.id == 322061619570016256:
            channel = 703665588244971582
            emoji = '\N{THUMBS UP SIGN}'
            emoji1 = '\N{THUMBS DOWN SIGN}'
            if message.channel.id == channel:
                await message.add_reaction(emoji)
                await asyncio.sleep(1)
                await message.add_reaction(emoji1)

    @commands.Cog.listener('on_message')
    async def SoD(self, message):
        if message.guild is None:
            return
        if message.guild.id == 322061619570016256:
            emoji2 = 'a:siren:789554809006325760'
            role1 = message.guild.get_role(703230475472207924)
            if role1.mention in message.content.lower():
                await message.channel.send('<a:siren:789554809006325760> **Staff on duty have been notified, please stand by.** <a:siren:789554809006325760>')
                await message.add_reaction(emoji2)
                await role.edit(mentionable=False, reason='Staff on duty role mentioned.')
                await asyncio.sleep(120)
                await role.edit(mentionable=True, reason='Cooldown reached - Role can be mentioned again.')

    @commands.Cog.listener('on_message')
    async def QoTD(self, message):
        if message.guild is None:
            return
        if message.guild.id == 322061619570016256:
            role = discord.Role
            role2 = message.guild.get_role(790631558976503830)
            if 653685492100890635 == message.channel.id and ('#QoTD') in message.content:
                if any(
                    # Questioner, Sever manager, Owner
                    role.id in [665930105909936139,
                                407585313129758720, 521372852952498179]
                    for role in message.author.roles
                ):
                    await message.channel.send(role2.mention)

    @tasks.loop(hours=24)
    async def quest_enq(self):
        dt = datetime.datetime
        now = dt.now()
        owner = self.bot.get_user(self.bot.owner_id)
        if now.weekday() == 5:
            await owner.send('<@414530505585721357> Don\'t forget to ask about questioners!')

    @quest_enq.before_loop
    async def before_qe(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=24)
    async def quest_pick(self):
        dt = datetime.datetime
        now = dt.now()
        owner = self.bot.get_user(self.bot.owner_id)
        if now.weekday() == 6:
            await owner.send('<@414530505585721357> Don\'t forget to pick a questioner!')

    @quest_pick.before_loop
    async def before_pick(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=['oo'], help='Would you like to not have your cut liked?', description='Your reason should be short and sweet.')
    async def opt_out(self, ctx, *, reason):
        def check(reaction, user):
            return user == ctx.author
        if reason.lower() in ['m0nster', 'monster', 'poo', 'pee']:
            await ctx.message.add_reaction('🚫')
            return
        elif 'help' in reason.lower():
            await ctx.send_help(ctx.command)
        msg = await ctx.send('Are you sure you want to opt out of having your cut liked? This isn\'t a **light** decision and mesub will be (now less) annoyed if he has to remove you from this list.\n```\nYou also agree that you will not be able to like other people\'s cuts.\n```')
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send('I don\'t have all day so I assumed you said no.')
            return
        if str(reaction.emoji) == '👎':
            await ctx.send('Oh, you changed your mind? Alrighty.')
            return
        await ctx.send('Ok, I\'ve sent your ID and reason to mesub. You will be updated in your DMs, you make sure they\'re on.')
        channel = self.bot.get_channel(790618543904915486)
        await channel.send(f'__**New request from: {str(ctx.author)}**__\nThe reason is:\n`{reason}`\nTheir ID is:')
        await channel.send(f"{ctx.author.id}")

    @commands.command(aliases=['oi'], help='Want to have your cut liked again?', description='Your reason should be a little longer and sweeter.')
    async def opt_in(self, ctx, *, reason):
        def check(reaction, user):
            return user == ctx.author
        if ctx.author.id not in self.bot.no_cut:
            await ctx.send('Why do you need to opt in? You\'ve not opted out from my records...')
            return
        msg = await ctx.send('Are you sure you want to opt back in to having your cut liked? This isn\'t a **light** decision and you won\'t be able to just opt out again.\n```\nIt does mean you can like other people\'s cuts again.\n```')
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send('I don\'t have all day so I assumed you said no.')
            return
        if str(reaction.emoji) == '👎':
            await ctx.send('Oh, you changed your mind? Alrighty.')
            return
        await ctx.send('Ok, I\'ve sent your ID and reason to mesub. You will be updated in your DMs, you make sure they\'re on.')
        channel = self.bot.get_channel(790618543904915486)
        await channel.send(f'__**New **opt in** request from: {str(ctx.author)}**__\nThe reason is:\n`{reason}`\nTheir ID is:')
        await channel.send(f"{ctx.author.id}")

    async def db_to_embed(self):
        list = []
        self.bot.db.row_factory = aiosqlite.Row
        x = await self.bot.db.execute('SELECT * FROM questioner;')
        row = await x.fetchall()
        for rows in row:
            user = self.bot.get_user(rows['id'])
            list.append(
                f"{str(user) + ' (' + str(rows['id']) + ')  ' + str(rows['times'])}")
        return None if not list else list

    @commands.check(k.lvl3)
    @commands.group(invoke_without_command=True)
    async def questioner(self, ctx, *questioners: discord.User):
        async with ctx.channel.typing():
            list = []
            self.bot.db.row_factory = aiosqlite.Row
            x = '\n'
            for person in questioners:
                query = await self.bot.db.execute('SELECT * FROM questioner WHERE ID=?;', (person.id,))
                row = await query.fetchone()
                if row is None:
                    list.append(f'{person} has not been a questioner')
                else:
                    list.append(
                        f"{person} has been a questioner `{row['times']}` time(s).")
        await ctx.send(f'```\n{x.join(str(item) for item in list)}\n```')

    @questioner.command(help='Lists questioners')
    async def list(self, ctx):
        x = '\n'
        paginator = commands.Paginator(prefix='```css\n')
        list = await self.db_to_embed()
        if list is not None:
            for item in list:
                paginator.add_line(item)
            formatted_questioners = x.join(str(item) for item in list)
        else:
            formatted_questioners = 'No questioners found.'
        for page in paginator.pages:
            await ctx.send(page)

    @questioner.command(help='Adds or edits a questioner to the list.',
                        description='The number will override (not add) the current number in the list')
    async def add(self, ctx, person: discord.User, times: float = 1):
        async with ctx.channel.typing():
            query = await self.bot.db.execute('SELECT * FROM questioner WHERE id=?;', (person.id,))
            row = await query.fetchone()
            if row is not None:
                await self.bot.db.execute('UPDATE questioner SET times=? WHERE id=?', (times, person.id))
                await self.bot.db.commit()
                await ctx.send(f'`{person}`, has now been questioner `{times}` times!')
                return
            else:
                await self.bot.db.execute('INSERT INTO questioner(id, times) VALUES(?,?)', (person.id, times))
                await self.bot.db.commit()
                await ctx.send(f'`{person}`, has now been added to the db and has been a questioner `{times}` times!')

    @questioner.command(help='Sets the questioner for daily reminders')
    async def remind(self, ctx, person: discord.User):
        if not person:
            await ctx.send(f'{person} is the current questioner!')
        await ctx.send(f'{person} is the current questioner!')
        self.bot.questioner = person

    @tasks.loop(hours=24)
    async def questioner_reminder(self):
        try:
            await self.bot.questioner.send(f'Hello **{self.bot.questioner.name}**, don\'t forget to send your daily question in <#653685492100890635>!')
        except Exception:
            channel = self.bot.get_channel(767416350552490025)
            await channel.send('Today\'s task has failed. Will retry tomorrow...')

    @questioner_reminder.before_loop
    async def before_remind(self):
        await self.bot.wait_until_ready()
        now = datetime.datetime.now().astimezone()
        next_run = now.replace(hour=6, minute=0, second=0)
        if next_run < now:
            next_run += datetime.timedelta(days=1)
        await discord.utils.sleep_until(next_run)


def setup(bot):
    bot.add_cog(TD(bot))
