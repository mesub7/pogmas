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
            if ctx.command.qualified_name in ("load", "unload", "reload", "status", "activity", "jsk py"):
                await ctx.send("Command execution failed: You are not the bot owner. (10 points for finding this command though.)")

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            channel = self.bot.get_channel(767416350552490025)
            await channel.send(f'An error occured with command `{ctx.command}` in cog `{ctx.cog}`.\
            \n The command was invoked in <#{ctx.channel.id}> by `{ctx.author}`.\nThe server this was invoked in was `{ctx.guild}`. \nJumplink to command execution: {ctx.message.jump_url} . \nException:')
            await channel.send(f'```py\n{traceback.format_exception(type(error), error, error.__traceback__)}```')
            embed = discord.Embed(title="⚠ An error occurred ⚠", colour=discord.Colour.red(), description="An unexpected error has occured, this should never happen. I have sent details to mesub#0556.")
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
