import discord
from discord.ext import commands
from random import randint
from discord.ext.commands.cooldowns import BucketType
import Cogs.Checks as k



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
         pog_level = randint(1, 99)
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

     @k.lvl3()
     @commands.cooldown(1,60,BucketType.member)
     @commands.max_concurrency(3, per=BucketType.guild, wait=False)
     @commands.command(description="Likes somebody's cut.", help="I like ya cut g!")
     async def cut(self, ctx, member:discord.Member=None):
         if member is None and ctx.author.id == self.bot.owner_id:
             await ctx.send("Why would you like your own cut mesub?")
             return
         elif member is None:
             member = ctx.author
             await ctx.send("Why would like your own cut silly.")
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
             return user.author.id == member.id
         cut_liked = await self.bot.wait_for('message', check=check)
         channel = cut_liked.channel
         await channel.send(f"<@{member.id}> New message from {ctx.author}:")
         await channel.send("https://tenor.com/view/cut-cut-g-ilike-ya-cut-g-meme-callmecarson-gif-18368253")
def setup(bot):
    bot.add_cog(Fun(bot))
