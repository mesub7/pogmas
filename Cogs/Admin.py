import discord
from discord.ext import commands
import asyncio
import Cogs.Checks as k



class Admin(commands.Cog):
    """The administrative cog. Most commands related to
    the operation and management of the bot are found here.
    """

    def __init__(self, bot):
        self.bot = bot
        level_4 = k.lvl4

    @commands.is_owner()
    @commands.command(description="Add a command alias.")
    async def swap(self, ctx, cmdname, alias):
        cmd = self.bot.get_command(cmdname)
        cmd.aliases.append(alias)
        # register the modified command
        self.bot.remove_command(cmdname)
        self.bot.add_command(cmd)
        await ctx.send('Done!')

    @commands.check(k.lvl5)
    @commands.command(description="Restarts the bot.")
    async def restart(self, ctx):
        await ctx.send("Ok! I'll restart now...")
        await self.bot.close()

    @commands.check(k.lvl5)
    @commands.command(name='disable', description="Disables a command.")
    async def _disable(self, ctx, command:str):
        c = self.bot.get_command(command)
        try:
            c.enabled = False
            await ctx.send(f"Command '{command}' disabled.")
        except Exception as e:
            await ctx.send("Command execution failed: Command not found.")


    @commands.check(k.lvl5)
    @commands.command(name='enable', description="Enables a command.")
    async def _enable(self, ctx, command:str):
        c = self.bot.get_command(command)
        try:
            c.enabled = True
            await ctx.send(f"Command '{command}' enabled.")
        except Exception as e:
            await ctx.send("Command execution failed: Command not found.")

    @commands.check(k.lvl4)
    @commands.command()
    async def say(self, ctx, channel:discord.TextChannel, *, words:str=None):
        file=[await attachment.to_file() for attachment in ctx.message.attachments]
        await ctx.message.delete()
        await channel.trigger_typing()
        if words is not None:
            if len(words) < 5:
                await asyncio.sleep(1)
            elif len(words) < 10:
                await asyncio.sleep(2)
            elif len(words) < 24:
                await asyncio.sleep(4)
            elif len(words) < 30:
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(6)
        await channel.send(words, files=file)

    @commands.check(k.lvl4)
    @commands.command()
    async def dm(self, ctx, member:discord.Member, *, words=None):
        user = member
        file=[await attachment.to_file() for attachment in ctx.message.attachments]
        await user.send(words, files=file)
        await ctx.message.delete()

    @commands.is_owner()
    @commands.command(name='load', description="Command which Loads a Module.")
    async def acog_load(self, ctx, *cogs: str):
        for cog in cogs:
            try:
                self.bot.load_extension(f'Cogs.{cog}')
            except Exception as e:
                await ctx.send(f'**`An error occured with loading cog {cog}:`** ```py\n{type(e).__name__} - {e}\n```')
            else:
                await ctx.send(f'`{cog}` has been loaded!')

    @commands.is_owner()
    @commands.command(name='unload', description="Command which Unloads a Module.")
    async def acog_unload(self, ctx, *cogs: str):
        for cog in cogs:
            try:
                self.bot.unload_extension(f'Cogs.{cog}')
            except Exception as e:
                await ctx.send(f'**`An error occured with unloading cog {cog}:`** ```py\n{type(e).__name__} - {e}\n```')
            else:
                await ctx.send(f'`{cog}` has been unloaded!')

    @commands.check(k.lvl5)
    @commands.command(name='reload', aliases=["hotload", "hl"], description="Command which Reloads a Module.")
    async def acog_reload(self, ctx, *cogs: str):
        if ('all') in cogs:
            for extension in self.bot.initial_extensions:
                try:
                    self.bot.reload_extension(extension)
                except Exception as e:
                    await ctx.send(f'**`An error occured with reloading cog {extension}:`** ```py\n{type(e).__name__} - {e}\n```')
            await ctx.send('All cogs have been reloaded! 🔥')
        else:
            try:
                for cog in cogs:
                    self.bot.reload_extension(f'Cogs.{cog}')
                    await ctx.send(f'`Cogs.{cog}` has been hot-loaded! 🔥')
            except Exception as e:
                await ctx.send(f'**`An error occured:`** ```py\n{type(e).__name__} - {e}\n```')

    @commands.check(k.lvl5)
    @commands.group(description="The legacy group commands for manual work.")
    async def legacy(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Command execution failed: Argument is missing! Correct usage:")
            await ctx.send_help(ctx.command)

    @commands.check(k.lvl5)
    @legacy.command(name='load', description="Loads an extension outside the `Cogs` folder. Can load an extension inside it as well.\
    \nRemember to use dot path. e.g: Cogs.Admin")
    async def lcog_load(self, ctx, *cogs: str):
        for cog in cogs:
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f'**`An error occured with loading {cog}:`** ```py\n{type(e).__name__} - {e}\n```')
            else:
                await ctx.send(f'`{cog}` has been loaded!')

    @commands.check(k.lvl5)
    @legacy.command(name='unload', description='Unloads an extension outside of the `Cogs` folder. Can unload an extension inside it as well.\
    \nRemember to use dot path. e.g: Cogs.Admin')
    async def lcog_unload(self, ctx, *cogs: str):
        for cog in cogs:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                await ctx.send(f'**`An error occured with unloading cog {cog}:`** ```py\n{type(e).__name__} - {e}\n```')
            else:
                await ctx.send(f'`{cog}` has been unloaded!')

    @commands.check(k.lvl5)
    @legacy.command(name='reload', aliases=['hl', 'hotload'], description='Reloads an extenson outside of the `Cogs` folder. Can reload an extension inside it as well.\
    \nRemember to use dot path. e.g: Cogs.Admin')
    async def lcog_reload(self, ctx, *cogs:str):
        try:
            for cog in cogs:
                self.bot.reload_extension(cog)
                await ctx.send(f'`{cog}` has been hot-loaded! 🔥')
        except Exception as e:
            await ctx.send(f'**`An error occured:`** ```py\n{type(e).__name__} - {e}\n```')

    @commands.check(k.lvl5)
    @commands.command(name="status", aliases=["online"], description="Sets the bot's status.")
    async def online(self, ctx, icon:str = None, status:str = None, *, words:str = None):
        if icon is None or icon.lower() in ("g", "online"):
            if status is None:
                await self.bot.change_presence(activity=None)
                await ctx.send("Activity set to nothing and status set to online!")
            elif status.lower() in ("playing", "p", "play", "game"):
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=words))
                await ctx.send(f"I will now play '{words}' and be online!")
            elif status.lower() in ("watching", "w", "watch", "tv"):
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=words))
                await ctx.send(f"I will now watch '{words}' and be online!")
            elif status.lower() in ("listening", "l", "listen", "song"):
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=words))
                await ctx.send(f"I will now listen to '{words}' and be online!")
            elif status.lower() in ("competing", "c", "compete", "battle"):
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name=words))
                await ctx.send(f"I will now compete in '{words}' and be online!")
            else:
                await ctx.send("Invalid option.")
        elif icon.lower() in ("idle","yellow", "away", "y"):
            if status is None:
                await self.bot.change_presence(status=discord.Status.idle)
                await ctx.send("Activity set to nothing and status set to idle!")
            elif status.lower() in ("playing", "p", "play", "game"):
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=words))
                await ctx.send(f"I will now play '{words}' and be idle!")
            elif status.lower() in ("watching", "w", "watch", "tv"):
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=words))
                await ctx.send(f"I will now watch '{words}' and be idle!")
            elif status.lower() in ("listening", "l", "listen", "song"):
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name=words))
                await ctx.send(f"I will now listen to '{words}' and be idle!")
            elif status.lower() in ("competing", "c", "compete", "battle"):
                await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.competing, name=words))
                await ctx.send(f"I will now compete in '{words}' and be idle!")
            else:
                await ctx.send("Invalid option.")
        elif icon.lower() in ("dnd", "red", "r"):
            if status is None:
                await self.bot.change_presence(status=discord.Status.dnd)
                await ctx.send("Activity set to nothing and status set to dnd!")
            elif status.lower() in ("playing", "p", "play", "game"):
                await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=words))
                await ctx.send(f"I will now play '{words}' and be dnd!")
            elif status.lower() in ("watching", "w", "watch", "tv"):
                await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=words))
                await ctx.send(f"I will now watch '{words}' and be dnd!")
            elif status.lower() in ("listening", "l", "listen", "song"):
                await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=words))
                await ctx.send(f"I will now listen to '{words}'! and be dnd")
            elif status.lower() in ("competing", "c", "compete", "battle"):
                await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name=words))
                await ctx.send(f"I will now compete in '{words}'! and be dnd")
            else:
                await ctx.send("Invalid option")
        else:
            await self.bot.change_presence(status=discord.Status.invisible)
            await ctx.send("Status set to offline!")

def setup(bot):
    bot.add_cog(Admin(bot))
