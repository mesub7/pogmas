import discord
from discord.ext import commands
import traceback
import sys

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This allows us to call the default error handler at any time
        async def ee():
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            py_error = traceback.format_exception(type(error), error, error.__traceback__)
            py_error = ''.join(py_error)
            channel = self.bot.get_channel(767416350552490025)
            await channel.send(f'An error occured with command `{ctx.command}` in cog `{ctx.cog.qualified_name}`.\
            \n The command was invoked in <#{ctx.channel.id}> by `{ctx.author}`.\nThe server this was invoked in was `{ctx.guild}`. \nJumplink to command execution: {ctx.message.jump_url} . \nException:')
            await channel.send(f'```py\n{py_error}```')
            embed = discord.Embed(title="⚠ An error occurred ⚠", colour=discord.Colour.red(), description="An unexpected error has occured, this should never happen. I have sent details to mesub#0556.")
            await ctx.send(embed=embed)

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        # For this error example we check to see where it came from...
        if isinstance(error, discord.ext.commands.errors.MissingAnyRole):
            if ctx.command.qualified_name in ("say", "dm"):  # Check if the command being invoked is in the list
                await ctx.send('Command execution failed: You do not have any authorised roles.\
                \nIf you think this is a mistake please contact `mesub#0556`.')

        elif isinstance(error, discord.ext.commands.errors.NotOwner):
            if ctx.command.qualified_name in ('jishaku py'):
                await ctx.send("Evaluation of **python** code can only be executed by the bot owner.")
            else:
                await ctx.send("Command execution failed: You are not the bot owner. (10 points for finding this command though.)")

        elif isinstance(error, discord.ext.commands.DisabledCommand):
            await ctx.send("Command execution failed: Command is disabled and cannot be run, sorry.")

        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            await ctx.send(f"Woah there {ctx.author.name}, you're going too fast. Try again in: {int(ctx.command.get_cooldown_retry_after(ctx))}s.")

        elif isinstance(error, discord.ext.commands.MaxConcurrencyReached):
            if ctx.command.qualified_name in ('cut'):
                await ctx.send("Command execution failed: All my hands are busy right now; I can only like `3` cuts per server at any one time!")
            else:
                await ee()

        elif isinstance(error, discord.ext.commands.BadArgument):
            if ctx.command.qualified_name in ("say"):
                await ctx.send("Command execution failed: Channel not found.")
            else:
                await ee()

        elif isinstance(error, discord.ext.commands.errors.TooManyArguments):
            if ctx.command.qualified_name in ("jishaku py"):
                await ctx.send("It's either: \n`eval`\n`jsk py` or\n`jishaku py`\nOkay?")
            else:
                await ee()

        elif isinstance(error, discord.ext.commands.DisabledCommand):
            if ctx.command.qualified_name in ("dm"):
                await ctx.send("Command execution failed: User not found.")
            else:
                await ee()

        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send("Command execution failed: Argument is missing! Correct usage:")
            await ctx.send_help(ctx.command)

        elif isinstance(error, discord.ext.commands.CommandError):
            if ctx.command.qualified_name in ("say", "dm"):
                await ctx.send("Command execution failed: You are not in the `lvl4` group of users authorised to use this command.\
                \nIf you think this is a mistake please contact mesub#0556.")
            elif ctx.command.qualified_name in ("cut"):
                await ctx.send("Command execution failed: You are not in the `lvl3` (Boosters or channel members) group of users authorised to use this command.\
                \nIf you think this is a mistake please contact mesub#0556.")
            else:
                await ee()

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            await ee()



def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
