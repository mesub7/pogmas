"""
Some of this code is from huantian which has kindly allowed me to use with the preservation of the MIT license below:

MIT License

Copyright (c) 2020 huantian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands
from random import randint, choice
from discord.ext.commands.cooldowns import BucketType
import Cogs.Checks as k
import datetime
import asyncio
import re
import magic8ball
import aiosqlite


class Fun(commands.Cog):
    """The Fun cog. Contains all sorts of games and enetertaining functions."""

    def __init__(self, bot):
         self.bot = bot
         level_3 = k.lvl3
         level_2 = k.lvl2
         self.bot.banned = []
         bot.loop.create_task(self.load_banned())

    async def load_banned(self):
        await self.bot.wait_until_ready()
        print('Loading banned words from database.')
        self.bot.db.row_factory = aiosqlite.Row
        query = await self.bot.db.execute('SELECT * FROM banned_words;')
        rows = await query.fetchall()
        for row in rows:
            self.bot.banned.append(f"{row['words']}")
        print('Banned words loaded!')

    @commands.command(description='Produces a random number from 1!', help='Produces a random number from 1!')
    async def random(self, ctx, limit=None):
        if limit is None:
            await ctx.send('I need a number!')
        else:
            try:
                result = randint(1, int(limit))
                await ctx.send('The result is: %s!' % result)
            except Exception as e:
                await ctx.send('Invalid number! It needs to be a **whole** positive number.')

    @commands.cooldown(3,60,BucketType.member)
    @commands.command(description='Checks how pog somebody is!', help='Checks how pog somebody is!')
    async def pog(self, ctx, member:discord.Member=None):
        pog_level = randint(1, 100)
        if pog_level == 100:
            if member is None:
                member = ctx.author
            await ctx.send(f'Well this time, I think that {member.name} is off the scale!')
        else:
            if member is None and ctx.author.id in [self.bot.owner_id, 240035755458691072, 555459418591068170]:
                await ctx.send('You are 100% pog! (As always 😉)')
            elif member is None:
                member = ctx.author
                await ctx.send(f'This time, I would say that you are {pog_level}% pog.')
            elif member.id == self.bot.user.id:
                await ctx.send('I am 100% pog. No question.')
            elif member.id == self.bot.owner_id:
                await ctx.send('mesub is 100% pog! (As always 😉)')
            elif member.id == 242730576195354624:
                await ctx.send('Auttaja is beyond pog 😍😍')
            elif member.id == 240035755458691072:
                await ctx.send('Squid is 100% squidpog.')
            elif member.id == 555459418591068170:
                await ctx.send('Armyman Liam is 100% pog. 💂‍♂️')
            else:
                await ctx.send(f'This time, I would say that {member.name} is {pog_level}% pog.')

    @commands.cooldown(3,60,BucketType.member)
    @commands.command(description='Checks how UWU somebody is.')
    async def uwu(self, ctx, member:discord.Member=None):
        uwu_level = randint(1, 100)
        if 0 <= uwu_level <= 25:
            uwu = 'owo'
        elif 26 <= uwu_level <= 50:
            uwu = 'OWO'
        elif 51 <= uwu_level <= 75:
            uwu = 'uwu'
        else:
            uwu = 'UWU'
        if uwu_level == 100:
            if member is None:
                member = ctx.author
            await ctx.send(f'Well this time, I think that {member.name} is uWu! (100%)')
        else:
            if member is None and ctx.author.id == self.bot.owner_id:
                await ctx.send('You are the top uWu (As always 😉)')
            elif member is None:
                member = ctx.author
                await ctx.send(f'This time, I would say that you are {uwu} ({uwu_level}%).')
            elif member.id == self.bot.user.id:
                await ctx.send('I do not participate in this.')
            elif member.id == self.bot.owner_id:
                await ctx.send('mesub is uWu.(As always 😉)')
            elif member.id == 242730576195354624:
                await ctx.send('Auttaja does not participate in this.')
            else:
                await ctx.send(f'This time, I would say that {member.name} is {uwu} ({uwu_level}%).')

    @commands.group(description='Ask Pogmas and get a response!')
    async def ask(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Command execution failed: Argument is missing! Correct usage:')
            await ctx.send_help(ctx.command)

    @ask.command(description='No nonsense. Get a yes, no or maybe answer.\
    \nThese answers are randomly generated and are advisory only. Mesub is not responsible for anything that happens as a result of you following the bot\'s advice.')
    async def basic(self, ctx, *, question):
        quest = re.sub(r'[.?!]', '', question)
        responses = ['y', 'n', 'm']
        pick = choice(responses)
        m = self.bot.get_user(242730576195354624) #auttaja
        await ctx.channel.trigger_typing()
        await asyncio.sleep(3)
        if any(x in question.lower() for x in self.bot.banned) or m.mentioned_in(ctx.message):
            await ctx.send('Your question contains matters of a sensitive nature, I wouldn\'t be able to asnwer it.')
            return
        if pick == 'y':
            await ctx.send(f'Yes you should definitely {quest}.')
        elif pick == 'n':
            await ctx.send(f'No you should not {quest}.')
        else:
            await ctx.send(f'Hmmm, maybe you should {quest}... Maybe not...')

    @ask.command(name='ball', description='Ask the ball?\
    \nThese answers are randomly generated and are advisory only. Mesub is not responsible for anything that happens as a result of you following the bot\'s advice.')
    async def _8ball(self, ctx, *, question):
        ball = magic8ball.list
        await ctx.channel.trigger_typing()
        m = self.bot.get_user(242730576195354624) #auttaja
        if any(x in question.lower() for x in self.bot.banned) or m.mentioned_in(ctx.message):
            await ctx.send('Your question contains matters of a sensitive nature, I wouldn\'t be able to asnwer it.')
            return
        await asyncio.sleep(3)
        await ctx.send(choice(ball))

    @commands.check(k.lvl5)
    @ask.command(name='add', description='Adds a banned word to the list.')
    async def _add(self, ctx, *words):
        async with ctx.channel.typing():
            failed = []
            for word in words:
                try:
                    await self.bot.db.execute('INSERT INTO banned_words VALUES(?);', (word,))
                    self.bot.banned.append(word)
                except Exception as e:
                    failed.append(word)
            await self.bot.db.commit()
            if not failed:
                await ctx.send('All words were added!')
            else:
                x = '\n'
                await ctx.send(f'Some words were not added...\n```\n{x.join(str(f) for f in failed)}\n```')

    @commands.check(k.lvl5)
    @ask.command(name='remove', description='Removes a banned word from the list')
    async def _remove(self, ctx, *words):
        async with ctx.channel.typing():
            failed=[]
            for word in words:
                try:
                    await self.bot.db.execute('DELETE FROM banned_words WHERE words=?;', (word,))
                    self.bot.banned.remove(word)
                except Exception as e:
                    failed.append(word)
            await self.bot.db.commit()
            if not failed:
                await ctx.send('All words were removed!')
            else:
                x = '\n'
                await ctx.send(f'Some words were not removed...\n```\n{x.join(str(f) for f in failed)}\n```')


    @commands.check(k.lvl5)
    @commands.command(description='Approves people to be added to the no cut list.')
    async def add(self, ctx, *ids:int):
        async with ctx.channel.typing():
            failed = []
            for id in ids:
                try:
                    await self.bot.db.execute('INSERT INTO cuts VALUES(?)', (id,))
                    self.bot.no_cut.append(id)
                    x = self.bot.get_user(id)
                    await x.send(f'**Your case has been updated:**\nOperator {ctx.author} has approved your request with reason `Valid`.\nYou will no longer have your cut liked')
                except aiosqlite.IntegrityError:
                    await ctx.send(f'User `{id}` was already inside the no-cut list!')
                except discord.Forbidden or discord.HTTPException:
                    failed.append(id)
            await self.bot.db.commit()
            if not failed:
                await ctx.send('User(s) were added!')
            else:
                x = '\n'
                await ctx.send(f'All users were added but users with the following IDs were not notified.\n```py\n{x.join(str(f) for f in failed)}\n```')

    @commands.check(k.lvl5)
    @commands.command(description='Removes somebody from the no cut list.')
    async def remove(self, ctx, *ids:int):
        async with ctx.channel.typing():
            failed = []
            for id in ids:
                try:
                    await self.bot.db.execute('DELETE FROM cuts WHERE id=?;', (id,))
                    self.bot.no_cut.remove(id)
                    x = self.bot.get_user(id)
                    await x.send(f'**Your case has been updated:**\nOperator {ctx.author} has approved your request with reason `Valid`.\nYou will now be able to have your cut liked.')
                except discord.Forbidden:
                    failed.append(id)
                except ValueError:
                    await ctx.send(f'User with ID `{id}` not in list!')
            await self.bot.db.commit()
            if not failed:
                await ctx.send('User(s) were removed!')
            else:
                x = '\n'
                await ctx.send(f'All users were removed but users with the following IDs were not notified.\n```py\n{x.join(str(f) for f in failed)}\n```')

    @commands.check(k.lvl5)
    @commands.command(description='Rejects somebody to be added to the no cut list.')
    async def deny(self, ctx, ids: commands.Greedy[discord.Member], *, reason='None'):
        for id in ids:
            try:
                await id.send(f'**Your case has been updated:**\nOperator {ctx.author} has denied your request with reason `{reason}`.\nYou may submit another request in 24 hours time.')
            except Exception as e:
                pass
        await ctx.send('Users denied!')

    @commands.cooldown(1,240,BucketType.member)
    @commands.max_concurrency(3, per=BucketType.guild, wait=False)
    @commands.max_concurrency(1, per=BucketType.member, wait=False)
    @commands.command(description='Likes somebody\'s cut.', help='I like ya cut g!')
    async def cut(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.author
            await ctx.send('Why would you like your own cut silly.')
            ctx.command.reset_cooldown(ctx)
            return
        elif member.id in self.bot.no_cut:
            await ctx.send('This user has opted out of having their cut liked.')
            ctx.command.reset_cooldown(ctx)
            return
        elif ctx.author.id in self.bot.no_cut:
            await ctx.send('Remember that you agreed you won\'t like people\'s cuts so they don\'t like yours...')
            ctx.command.reset_cooldown(ctx)
            return
        elif member is None and ctx.author.id == self.bot.owner_id:
            await ctx.send('Why would you like your own cut mesub?')
            ctx.command.reset_cooldown(ctx)
            return
        elif member.bot:
            await ctx.send('As part of the Discord Bot Framework Agreement 2017, I cannot like another bot\'s cut.')
            ctx.command.reset_cooldown(ctx)
            return
        elif member.id == self.bot.user.id:
            await ctx.send('Glad you like it! (What would you think would happen?)')
            ctx.command.reset_cooldown(ctx)
            return
        elif member.id == self.bot.owner_id:
            await ctx.send('Command exucution failed: mesub\'s cut cannot be liked.')
            ctx.command.reset_cooldown(ctx)
            return
        else:
            await ctx.send('Cut liked 👌.')
        def check(user):
            return user.author.id == member.id and user.channel.category_id not in [497794660681646101, 653685359460483093]
        try:
            cut_liked = await self.bot.wait_for('message', check=check, timeout=7200.0)
            channel = cut_liked.channel
        except Exception as error:
            error = getattr(error, 'original', error)
            if isinstance(error, asyncio.TimeoutError):
                await ctx.send(f'{ctx.author.mention}, I got bored of waiting for them so I cancelled it.')
                return
            else:
                await ctx.send(f'{ctx.author.mention}, I can\'t like their cut for reasons beyond my control.')
                return
        await channel.send(f'<@{member.id}> <a:slap:790598778699776090>!')
        await channel.send(f'You were slapped by {ctx.author}')

    @commands.command(help='How many days until Christmas?!?!')
    async def days(self, ctx):
        dt  = datetime.datetime
        now = dt.now()
        cd=dt(year=now.year, month=12,day=25) - dt(year=now.year, month=now.month, day=now.day)
        await ctx.send(f'There are `'+str(cd)[:str(cd).find(',')]+'` until Christmas. 🎄')


    @commands.command(help='Can you avoid the ghosts?', name='ghost', aliases=['gg'])
    async def gg(self, ctx):
        feeling_brave = True
        score = 0
        while feeling_brave:
            if score == 0:
                await ctx.send('__**Ghost Game**__\nThree doors ahead...\nA ghost behind one\n Which one do you choose.. 1, 2 or 3?')
            else:
                await ctx.send('Three doors ahead...\nA ghost behind one\n Which one do you choose.. 1, 2 or 3?')
            gdoor = randint(1,3)
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content in ('1', '2', '3')
            try:
                s = await self.bot.wait_for('message', check=check, timeout=30.0)
                door = int(s.content)
            except asyncio.TimeoutError:
                feeling_brave = False
                await ctx.send(f'Game over: you took too long. Score `{score}`.')
                return
            if door == gdoor:
                await ctx.send('Ghost! 👻\nRun away!')
                await ctx.send(f'Game over. Score: `{score}`.')
                feeling_brave = False
            else:
                await ctx.send('No ghost!\nYou enter the next room...')
                score = score + 1

    @commands.cooldown(3,40,BucketType.member)
    @commands.command(help='Produces a random shaun from the mini-bank!')
    async def shaun(self, ctx):
        list = ['<:shaunup:810532538241122335>', '<:shauntrain:810532539596537906>', '<:shaunra:810532540808167464>', '<:shaunpm:810532540183478332>', '<:shaunold:810532539634548736>',\
         '<:shaunit:810532536458543114>', '<:shaunhug:810532540594389022>', '<:shaunhand:810532537449185350>', '<:shaun2:810532534982279169>', '<:shaun:810534623351537665>']
        await ctx.send(f'This time, it\'s {choice(list)}!')


    @commands.guild_only()
    @commands.command(help='Can you react in time?')
    async def thumbs(self, ctx):
        score = 0
        good_terms = True
        bank = ['🚒','😄','😉','🥛','🍼','😘','🤗','🤔','😍','😡','😱','🦷','👀','🦈','🍫','🍓','🍍','🍎','🚍','🚌', '😎']
        names = ['Cocker', 'm8', 'fam', 'mandem', 'bro', 'g', 'guy']
        try:
            await ctx.message.delete()
        except Exception as e:
            pass
        emoji = choice(bank)
        name = choice(names)
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emoji
        while good_terms:
            if score == 0:
                msg = await ctx.send(f'Send me that {emoji} reaction, Cocker.')
            else:
                emoji = choice(bank)
                name = choice(names)
                msg = await ctx.send(f'Send me that {emoji} reaction, {name}')
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=randint(8,20), check=check)
            except asyncio.TimeoutError:
                await msg.delete()
                await ctx.send('Slow! :snail:')
                await ctx.send(f'Game over! Your score was `{score}`')
                good_terms = False
                return
            else:
                await ctx.send(f'Good job {ctx.author.name} :thumbsup:')
                try:
                    await msg.delete()
                except Exception as e:
                    pass
                bank.remove(emoji)
                score = score + 1
            if not bank:
                await ctx.send(f'You\'ve beat the game, {ctx.author.name}! Good work.\nYour score is {score}.')
                good_terms = False
                return
# Tic tac toe stuff
    global emoji_dict
    emoji_dict = {
    '↖️': 0,
    '⬆️': 1,
    '↗️': 2,
    '⬅️': 3,
    '⏺️': 4,
    '➡️': 5,
    '↙️': 6,
    '⬇️': 7,
    '↘️': 8
}


    def make_grid_internals(self, grid):
        """Converts the normal grid list into human-readable version."""
		# Replace all values in the grid list with emojis
        new_grid = [':white_large_square:' if not x
                else ':regional_indicator_x:' if x == 1
                else ':o2:' if x == 2
                else '?'
                for x in grid]


		# Adds a new line every three emojis.
        return '\n'.join(''.join(new_grid[i:i + 3]) for i in range(0, len(new_grid), 3))




    async def draw_grid(self, channel, message, grid, player1, player2, current_player):
        """Draws the initial grid of the game."""
        grid = self.make_grid_internals(grid)
        current_player = player1 if current_player == 1 else player2
        self.bot.ttt_description = f'**Tic-Tac-Toe game between** `{str(player1)}` **and** `{str(player2)}`\n\n`{str(player1)}`: \U0001f1fd\n`{str(player2)}`: 🅾\n\nCurrent turn: {current_player.mention}.'


        return await message.edit(content=f'{self.bot.ttt_description}\n\n**Grid:**\n{grid}')


    async def edit_grid(self, message, grid, player1, player2, current_player):
        grid = self.make_grid_internals(grid)

        current_player = player1 if current_player == 1 else player2
        self.bot.ttt_description = f'**Tic-Tac-Toe game between** `{str(player1)}` **and** `{str(player2)}`\n\n`{str(player1)}`: \U0001f1fd\n`{str(player2)}`: 🅾\n\nCurrent turn: {current_player.mention}.'
        await message.edit(content=f'{self.bot.ttt_description}\n\n**Grid:**\n{grid}')


    async def edit_grid_end(self, message, grid, player1, player2, current_player, end_message):
        grid = self.make_grid_internals(grid)

        current_player = player1 if current_player == 1 else player2
        description_end = f'**Tic-Tac-Toe game between** `{str(player1)}` **and** `{str(player2)}`\n\n`{str(player1)}`: \U0001f1fd\n`{str(player2)}`: 🅾\n\n{end_message}'

        await message.edit(content=f'{description_end}\n\n**Grid:**\n{grid}')


    def win_indexes(self, n):
		# Rows
        for r in range(n):
            yield [(r, c) for c in range(n)]
		# Columns
        for c in range(n):
            yield [(r, c) for r in range(n)]
		# Diagonal top left to bottom right
        yield [(i, i) for i in range(n)]
		# Diagonal top right to bottom left
        yield [(i, n - 1 - i) for i in range(n)]


    def is_winner(self, board, decorator):
        n = len(board)
        for indexes in self.win_indexes(n):
            if all(board[r][c] == decorator for r, c in indexes):
                return True
        return False


    def check_for_end(self, grid):
        if 0 not in grid:
            if self.is_winner([grid[i:i + 3] for i in range(0, len(grid), 3)], 1):
                return 1
            elif self.is_winner([grid[i:i + 3] for i in range(0, len(grid), 3)], 2):
                return 2
            return 'draw'
        elif self.is_winner([grid[i:i + 3] for i in range(0, len(grid), 3)], 1):
            return 1
        elif self.is_winner([grid[i:i + 3] for i in range(0, len(grid), 3)], 2):
            return 2
        else:
            return

    @commands.guild_only()
    @commands.command()
    async def ttt(self, ctx, player2: commands.MemberConverter):
        """Starts a Tic-Tac-Toe game with the specified player!"""
        player1 = ctx.author
        current_player = randint(1, 2)
        running = True
        used_emojis = []
        counter = 0

		# Makes sure that the player isn't a bot.
        if player2.bot:
            await ctx.send('You can\'t play against a bot!')
            return

        if player2 == ctx.author:
            await ctx.send('You can\'t play against yourself you cheat!')
            return

        sure = await ctx.send(f'{player2.mention}, **{str(ctx.author)}** has challenged you to a game of **Tic-Tac-Toe.**\nDo you accept?')
        def check_x(reaction, user):
            return user == player2
        await sure.add_reaction('👍')
        await sure.add_reaction('👎')
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check_x, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send('I see you took too long so I cancelled it...')
            return
        if str(reaction.emoji) == '👎':
            await ctx.send('Oh? You\'re not up for it? All good.')
            return
		# Creates and sends the initial grid
        message = await ctx.send('Preparing the grid, one second...')
        grid = [0 for x in range(9)]
        for emoji in emoji_dict:
            await message.add_reaction(emoji)

        await self.draw_grid(ctx.channel, message, grid, player1, player2, current_player)

		# Adds all the emojis to make moves

		# Running loop, continuously checks for new inputs until someone wins
        while running:
			# Makes a usable object based on current player
            current_player_object = player1 if current_player == 1 else player2

            def check(r, u):
				# Checks that it is a valid emoji, that the emoji wasn't used before, and that it is the current player
                return (r.emoji in emoji_dict) and (r.emoji not in used_emojis) and (u == current_player_object)

		# Waits for a reaction, edits grid and used emojis accordingly
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                running = False
                await ctx.send(f'Game canceled as `{str(current_player_object)}` took too long.')
                return
            else:
                grid[emoji_dict[reaction.emoji]] = 1 if current_player == 1 else 2 if current_player == 2 else '??'
                used_emojis.append(reaction.emoji)

            end = self.check_for_end(grid)
            if end == 'draw':
                await self.edit_grid_end(message, grid, player1, player2, current_player, 'It\'s a draw!')
                running = False
            elif end == 1:
                await self.edit_grid_end(message, grid, player1, player2, current_player, f'{player1.mention} has won!')
                running = False
            elif end == 2:
                await self.edit_grid_end(message, grid, player1, player2, current_player, f'{player2.mention} has won!')
                running = False
            else:
				# Switch current player to next player
                current_player = 2 if current_player == 1 else 1
				# Update grid with new information
                await self.edit_grid(message, grid, player1, player2, current_player)

def setup(bot):
    bot.add_cog(Fun(bot))
