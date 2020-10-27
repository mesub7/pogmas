import discord
from discord.ext import commands
import asyncio

class Admin(commands.Cog):
     def __init__(self, bot):
        self.bot = bot

     @commands.command(hidden=True)
     async def restart(self, ctx):
          bot_owner_id = 414530505585721357
          if ctx.author.id == bot_owner_id:
               message = await ctx.send("Ok! I'll restart now...")
               await self.bot.close()
          else:
               await ctx.send("You don't need to use this command :)")

     async def lvl4(ctx):
         return ctx.author.id in (252504297772679168, 378924582452723734, 325357652752203777, 240035755458691072,\
         439784355343237151, 290619509641838603, 390978899645038602, 414530505585721357)

     @commands.command(hidden=True)
     @commands.check(lvl4)
     async def say(self, ctx, channel:discord.TextChannel, *, words:str):
          await ctx.message.delete()
          await channel.trigger_typing()
          if len(words) < 5:
              await asyncio.sleep(1)
          elif len(words) < 10:
              await asyncio.sleep(2)
          elif len(words) < 24:
              await asyncio.sleep(4)
          else:
              await asyncio.sleep(6)
          await channel.send(words)




     @commands.command(hidden=True)
     @commands.check(lvl4)
     async def dm(self, ctx, member:discord.Member, *, words):
         user = member
         await user.send(words)
         await ctx.message.delete()



     @commands.command(name='load', hidden=True, description="Command which Loads a Module.\
     Remember to use dot path. e.g: Cogs.Admin")
     @commands.is_owner()
     async def acog_load(self, ctx, *, cog: str):
         try:
             self.bot.load_extension(cog)
         except Exception as e:
             await ctx.send(f'**`An error occured:`** ```py\n{type(e).__name__} - {e}\n```')
         else:
             await ctx.send(f'`{cog}` has been loaded!')

     @commands.command(name='unload', hidden=True, description="Command which Unloads a Module.\
     Remember to use dot path. e.g: Cogs.Admin")
     @commands.is_owner()
     async def acog_unload(self, ctx, *, cog: str):
         try:
             self.bot.unload_extension(cog)
         except Exception as e:
             await ctx.send(f'**`An error occured:`** ```py\n{type(e).__name__} - {e}\n```')
         else:
             await ctx.send(f'`{cog}` has been unloaded!')

     @commands.command(name='reload', hidden=True, aliases=["hotload", "hl"], description="Command which Reloads a Module.\
     Remember to use dot path. e.g: Cogs.Admin")
     @commands.is_owner()
     async def acog_reload(self, ctx, *, cog: str):
         try:
             self.bot.reload_extension(cog)
         except Exception as e:
             await ctx.send(f'**`An error occured:`** ```py\n{type(e).__name__} - {e}\n```')
         else:
             await ctx.send(f'`{cog}` has been hot-loaded! 🔥')

     @commands.is_owner()
     @commands.command(name="status", hidden=True, aliases=["online"])
     async def online(self, ctx, icon:str = None, status:str = None, *, words:str = None):
         if icon.lower() in (None,"g", "online"):
             if status is None:
                 await self.bot.change_presence(activity=None)
                 await ctx.send("Activity set to nothing and status set to online!")
             elif status.lower() in ("playing", "p", "play", "game"):
                 await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=words))
                 await ctx.send(f"I will now play {words} and be online!")
             elif status.lower() in ("watching", "w", "watch", "tv"):
                 await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=words))
                 await ctx.send(f"I will now watch {words} and be online!")
             elif status.lower() in ("listening", "l", "listen", "song"):
                 await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=words))
                 await ctx.send(f"I will now listen to {words} and be online!")
             elif status.lower() in ("competing", "c", "compete", "battle"):
                 # await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name=words))
                 await ctx.send("Hang on! (will be in next update.)")
             else:
                 await ctx.send("Invalid option.")
         elif icon.lower() in ("idle","yellow", "away", "y"):
             if status is None:
                 await self.bot.change_presence(status=discord.Status.idle)
                 await ctx.send("Activity set to nothing and status set to idle!")
             elif status.lower() in ("playing", "p", "play", "game"):
                 await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=words))
                 await ctx.send(f"I will now play {words} and be idle!")
             elif status.lower() in ("watching", "w", "watch", "tv"):
                 await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=words))
                 await ctx.send(f"I will now watch {words} and be idle!")
             elif status.lower() in ("listening", "l", "listen", "song"):
                 await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name=words))
                 await ctx.send(f"I will now listen to {words} and be idle!")
             elif status.lower() in ("competing", "c", "compete", "battle"):
                 # await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.competing, name=words))
                 await ctx.send("Hang on! (will be in next update.)")
             else:
                 await ctx.send("Invalid option.")
         elif icon.lower() in ("dnd", "red", "r"):
             if status is None:
                 await self.bot.change_presence(status=discord.Stauts.dnd)
                 await ctx.send("Activity set to nothing and status set to dnd!")
             elif status.lower() in ("playing", "p", "play", "game"):
                 await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=words))
                 await ctx.send(f"I will now play {words} and be dnd!")
             elif status.lower() in ("watching", "w", "watch", "tv"):
                 await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=words))
                 await ctx.send(f"I will now watch {words} and be dnd!")
             elif status.lower() in ("listening", "l", "listen", "song"):
                 await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=words))
                 await ctx.send(f"I will now listen to {words}! and be dnd")
             elif status.lower() in ("competing", "c", "compete", "battle"):
                 # await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name=words))
                 await ctx.send("Hang on! (will be in next update.)")
             else:
                 await ctx.send("Invalid option")
         else:
             await self.bot.change_presence(status=discord.Status.invisible)
             await ctx.send("Status set to offline!")

def setup(bot):
    bot.add_cog(Admin(bot))
