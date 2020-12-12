"""
Some of this code is from huantian which has kindly allowed me to use with the preservation of the MIT license below:

MIT License

Copyright (c) 2020 huantian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
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


class Fun(commands.Cog):
    def __init__(self, bot):
         self.bot = bot
         level_3 = k.lvl3
    global bot_owner_id


    @commands.command(description="Produces a random number from 1!", help="Produces a random number from 1!")
    async def random(self, ctx, limit=None):
        if limit is None:
            await ctx.send("I need a number!")
        else:
            result = randint(1, int(limit))
            await ctx.send("The result is: %s!" % result)

    @commands.cooldown(3,60,BucketType.member)
    @commands.command(description="Checks how pog somebody is!", help="Checks how pog somebody is!")
    async def pog(self, ctx, member:discord.Member=None):
        pog_level = randint(1, 100)
        if pog_level == 100:
            await ctx.send(f"Well this time, I think that {member.name} is off the scale!")
        else:
            if member is None and ctx.author.id == self.bot.owner_id:
                await ctx.send("You are 100% pog! (As always 😉)")
            elif member is None:
                member = ctx.author
                await ctx.send(f"This time, I would say that you are {pog_level}% pog.")
            elif member.id == self.bot.user.id:
                await ctx.send("I am 100% pog. No question.")
            elif member.id == self.bot.owner_id:
                await ctx.send("mesub is 100% pog! (As always 😉)")
            elif member.id == 242730576195354624:
                await ctx.send("Auttaja is beyond pog 😍😍")
            else:
                await ctx.send(f"This time, I would say that {member.name} is {pog_level}% pog.")


    @commands.cooldown(1,240,BucketType.member)
    @commands.max_concurrency(3, per=BucketType.guild, wait=False)
    @commands.max_concurrency(1, per=BucketType.member, wait=False)
    @commands.command(description="Likes somebody's cut.", help="I like ya cut g!")
    async def cut(self, ctx, member:discord.Member=None):
        if member is None and ctx.author.id == self.bot.owner_id:
            await ctx.send("Why would you like your own cut mesub?")
            return
        elif member is None:
            member = ctx.author
            await ctx.send("Why would you like your own cut silly.")
            return
        elif member.bot:
            await ctx.send("As part of the Discord Bot Framework Agreement 2017, I cannot like another bot's cut.")
            return
        elif member.id == self.bot.user.id:
            await ctx.send("Glad you like it! (What would you think would happen?)")
            return
        elif member.id == self.bot.owner_id:
            await ctx.send("Command exucution failed: mesub's cut cannot be liked.")
            return
        elif member.id == 242730576195354624:
            await ctx.send("I refuse to like Auttaja's cut.")
            return
        else:
            await ctx.send("Cut liked 👌.")
        def check(user):
            return user.author.id == member.id and user.channel.category_id not in [497794660681646101, 653685359460483093]
        try:
            cut_liked = await self.bot.wait_for('message', check=check, timeout=7200.0)
            channel = cut_liked.channel
        except Exception as error:
            error = getattr(error, 'original', error)
            if isinstance(error, asyncio.TimeoutError):
                await ctx.send(f"{ctx.author.mention}, I got bored of waiting for them so I cancelled it.")
                return
            else:
                await ctx.send(f"{ctx.author.mention}, I can't like their cut for reasons beyond my control.")
                return
        await channel.send(f"<@{member.id}> New message from {ctx.author}:")
        await channel.send("https://tenor.com/view/cut-cut-g-ilike-ya-cut-g-meme-callmecarson-gif-18368253")

    @commands.command(help="How many days until Christmas?!?!")
    async def days(self, ctx):
        dt  = datetime.datetime
        now = dt.now()
        cd=dt(year=now.year, month=12,day=25) - dt(year=now.year, month=now.month, day=now.day)
        await ctx.send(f'There are `'+str(cd)[:str(cd).find(",")]+'` until Christmas. 🎄')

    @commands.command(help="How many days until Brexit?!?!")
    async def brexit(self, ctx):
        dt  = datetime.datetime
        now = dt.now()
        cd=dt(year=2021, month=1,day=1) - dt(year=now.year, month=now.month, day=now.day)
        await ctx.send(f'There are `'+str(cd)[:str(cd).find(",")]+'` until <:BR:772541846357278791><:EX:772541846358196254><:IT:756911540728496220>')

    @k.lvl2()
    @commands.command(help="Can you avoid the ghosts?", name="ghost", aliases=['gg'])
    async def gg(self, ctx):
        feeling_brave = True
        score = 0
        while feeling_brave:
            if score == 0:
                await ctx.send("__**Ghost Game**__\nThree doors ahead...\nA ghost behind one\n Which one do you choose.. 1, 2 or 3?")
            else:
                await ctx.send("Three doors ahead...\nA ghost behind one\n Which one do you choose.. 1, 2 or 3?")
            gdoor = randint(1,3)
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content in ("1", "2", "3")
            try:
                s = await self.bot.wait_for('message', check=check, timeout=30.0)
                door = int(s.content)
            except asyncio.TimeoutError:
                feeling_brave = False
                await ctx.send(f"Game over: you took too long. Score `{score}`.")
                return
            if door == gdoor:
                await ctx.send("Ghost! 👻\nRun away!")
                await ctx.send(f"Game over. Score: `{score}`.")
                feeling_brave = False
            else:
                await ctx.send("No ghost!\nYou enter the next room...")
                score = score + 1

    @commands.cooldown(3,40,BucketType.member)
    @commands.command(help="Produces a random shaun from the mini-bank!")
    async def shaun(self, ctx):
        list = ['<:shaunusa:774986283381948466>', '<:shaunup:774986279133773834>', '<:shauntrain:774986281217425428>',\
        '<:shaunra:774987341142949929>', '<:shaunpm:774986282682155018>', '<:shaunold:774986281334997012>', '<:shaunit:774986278004850689>',\
        '<:shaunhug:774986283835326466>', '<:shaunhand:774987343353479219>', '<:shaun2:774986280073166900>', '<:shaun:699731917729300603>']
        await ctx.send(f"This time, it's {choice(list)}!")

    @k.lvl2()
    @commands.guild_only()
    @commands.command(help="Can you react in time?")
    async def thumbs(self, ctx):
        await ctx.message.delete()
        msg = await ctx.send('Send me that :thumbsup: reaction, Cocker')
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '\U0001f44d'
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=randint(1,15), check=check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send('Fail! :thumbsdown:')
        else:
            await msg.delete()
            await ctx.send(f"Congrats "+str(ctx.author.mention)+" You Did It! :thumbsup:")
# Tic tac toe stuff
    global emoji_dict
    emoji_dict = {
    u"\u2196": 0,
    u"\u2B06": 1,
    u"\u2197": 2,
    u"\u2B05": 3,
    u"\u23FA": 4,
    u"\u27A1": 5,
    u"\u2199": 6,
    u"\u2B07": 7,
    u"\u2198": 8
}


    def make_grid_internals(self, grid):
        """Converts the normal grid list into human-readable version."""
		# Replace all values in the grid list with emojis
        new_grid = [":white_large_square:" if (not x)
                else ":regional_indicator_x:" if x == 1
                else ":o2:" if x == 2
                else "?"
                for x in grid]


		# Adds a new line every three emojis.
        return "\n".join("".join(new_grid[i:i + 3]) for i in range(0, len(new_grid), 3))




    async def draw_grid(self, channel, message, grid, player1, player2, current_player):
        """Draws the initial grid of the game."""
        grid = self.make_grid_internals(grid)
        current_player = player1 if current_player == 1 else player2
        self.bot.ttt_description = f"**Tic-Tac-Toe game between** `{str(player1)}` **and** `{str(player2)}`\n\n`{str(player1)}`: \U0001f1fd\n`{str(player2)}`: 🅾\n\nCurrent turn: {current_player.mention}."


        return await message.edit(content=f"{self.bot.ttt_description}\n\n**Grid:**\n{grid}")


    async def edit_grid(self, message, grid, player1, player2, current_player):
        grid = self.make_grid_internals(grid)

        current_player = player1 if current_player == 1 else player2
        self.bot.ttt_description = f"**Tic-Tac-Toe game between** `{str(player1)}` **and** `{str(player2)}`\n\n`{str(player1)}`: \U0001f1fd\n`{str(player2)}`: 🅾\n\nCurrent turn: {current_player.mention}."
        await message.edit(content=f"{self.bot.ttt_description}\n\n**Grid:**\n{grid}")


    async def edit_grid_end(self, message, grid, player1, player2, current_player, end_message):
        grid = self.make_grid_internals(grid)

        current_player = player1 if current_player == 1 else player2
        description_end = f"**Tic-Tac-Toe game between** `{str(player1)}` **and** `{str(player2)}`\n\n`{str(player1)}`: \U0001f1fd\n`{str(player2)}`: 🅾\n\n{end_message}"

        await message.edit(content=f"{description_end}\n\n**Grid:**\n{grid}")


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
            return "draw"
        elif self.is_winner([grid[i:i + 3] for i in range(0, len(grid), 3)], 1):
            return 1
        elif self.is_winner([grid[i:i + 3] for i in range(0, len(grid), 3)], 2):
            return 2
        else:
            return

    @k.lvl2()
    @commands.guild_only()
    @commands.command()
    async def ttt(self, ctx, player2: commands.MemberConverter):
        """Starts a Tic-Tac-Toe game with the specified player!"""
        player1 = ctx.author
        current_player = 1
        running = True
        used_emojis = []
        counter = 0

		# Makes sure that the player isn't a bot.
        if player2.bot:
            await ctx.send("You can't play against a bot!")
            return

        if player2 == ctx.author:
            await ctx.send("You can't play against yourself you cheat!")
            return

        sure = await ctx.send(f"{player2.mention}, **{str(ctx.author)}** has challenged you to a game of **Tic-Tac-Toe.**\nDo you accept?")
        def check_x(reaction, user):
            return reaction.emoji == '👍' and user == player2
        await sure.add_reaction('👍')
        await sure.add_reaction('👎')
        try:
            await self.bot.wait_for('reaction_add', check=check_x, timeout=20.0)
        except asyncio.TimeoutError:
            await ctx.send("I see you're not up for it so I cancelled it...")
            return
		# Creates and sends the initial grid
        message = await ctx.send("Preparing the grid, one second...")
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
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60.0)
            except asyncio.TimeoutError:
                running = False
                await ctx.send(f"Game canceled as `{str(current_player_object)}` took too long.")
                return
            else:
                grid[emoji_dict[reaction.emoji]] = 1 if current_player == 1 else 2 if current_player == 2 else "??"
                used_emojis.append(reaction.emoji)

            end = self.check_for_end(grid)
            if end == "draw":
                await self.edit_grid_end(message, grid, player1, player2, current_player, "It's a draw!")
                running = False
            elif end == 1:
                await self.edit_grid_end(message, grid, player1, player2, current_player, f"{player1.mention} has won!")
                running = False
            elif end == 2:
                await self.edit_grid_end(message, grid, player1, player2, current_player, f"{player2.mention} has won!")
                running = False
            else:
				# Switch current player to next player
                current_player = 2 if current_player == 1 else 1
				# Update grid with new information
                await self.edit_grid(message, grid, player1, player2, current_player)

def setup(bot):
    bot.add_cog(Fun(bot))
