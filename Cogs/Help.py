import discord
from discord.ext import commands

class PogmasHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'help': 'Shows help about the bot, a command, a cog or a category'  # This is the command.help string
})
    def get_command_signature(self, command):
        """Method to return a commands name and signature"""
        if not command.signature and not command.parent:  # no args and isn't a subcommand
            return f'{self.clean_prefix}{command.name}'
        if command.signature and not command.parent:  # args and isn't a subcommand
            return f'{self.clean_prefix}{command.name} {command.signature}'
        if not command.signature and command.parent:  # no args and is a subcommand
            return f'{self.clean_prefix}{str(command.parent)}{command.name}'
        else:  # it has args a signature and is a subcommand (possibly)
            return f'{self.clean_prefix}{str(command.parent)} {command.name} {command.signature}'

    def get_command_aliases(self, command):  # Gobot's method
        """Method to return a commands aliases"""
        if not command.aliases:  # check if it has any aliases
            return ''
        else:
            return f'Aliases - [{" | ".join([alias for alias in command.aliases])}]'

    def get_command_description(self, command):
        """Method to return a commands description"""
        if not command.description:  # check if it has any brief
            if command.help:
                return command.help
            else:
                return '\u2800'
        else:
            return command.description

    def get_command_help(self, command):
        """Method to return a commands full description/doc string"""
        if not command.help:  # check if it has any brief or doc string
            return ''
        else:
            return command.help

    async def send_command_help(self, command):
        ctx = self.context
        bot = ctx.bot
        if await command.can_run(ctx): # Can it be run?
            embed = discord.Embed(title=f'{command}', description=f'```\nUsage: {self.get_command_signature(command)}\n{self.get_command_aliases(command)}\n\n{self.get_command_description(command)}\n```',
            color=discord.Colour.blue())
            await ctx.send(embed=embed)
        else:
            if command.qualified_name in ('say', 'dm'):
                await ctx.send(f"No command called \"{command}\" found.")
            else:
                await ctx.send("Command execution failed: You do not have the required permissions to run this command. Therefore you are not permitted to see its help.")

    def add_extra(self, group):
        if group.invoke_without_command: # Add extra stuff for groups
            return '[subcommand] [args]'
        else:
            return '<subcommand> [args]'

    def get_group_help(self, group):
        if group.help:
            return group.help
        elif group.short_doc:
            return group.short_doc
        elif group.description:
            return group.description
        else:
            return ''

    async def send_group_help(self, group):
        ctx = self.context
        bot = ctx.bot
        all_commands = [command for command in await self.filter_commands(group.walk_commands(), sort=True)] # Still checking if they can run anything
        if not all_commands:
            await ctx.send("Command execution failed: You do not have the required permissions to run this group command (or any of its subcommands) so there is nothing to show.")
        else:
            embed = discord.Embed(title=f'{group.qualified_name}', description=f'```\nUsage: {self.clean_prefix}{group.qualified_name} {self.add_extra(group)}\n\n{self.get_group_help(group)}\n```',
            color=discord.Colour.blue())
            for c in all_commands:
                if not c.hidden:
                    signature = self.get_command_signature(c)
                    description = self.get_command_description(c)
                    if c.parent:  # it is a sub-command
                        embed.add_field(name=f'**╚╡**{signature}', value=description)
            await ctx.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        bot = ctx.bot
        all_commands = [command for command in await self.filter_commands(cog.walk_commands(), sort=True)] # Again. checking if they can run anything
        if not all_commands:
            await ctx.send("Command execution failed: You cannot run any commands in this cog so there is nothing to show.")
        else:
            embed = discord.Embed(title=f'Help with {cog.qualified_name}',
            description=cog.description, color=discord.Colour.blue())
            embed.set_thumbnail(url=ctx.bot.user.avatar_url)
            for c in all_commands:
                if not c.hidden:
                    signature = self.get_command_signature(c)
                    description = self.get_command_description(c)
                    if c.parent:  # it is a sub-command
                        embed.add_field(name=f'**╚╡**{signature}', value=description)
                    else:
                        embed.add_field(name=signature, value=description, inline=False)
            embed.set_footer(text=f'Use "{self.clean_prefix}help <command>" for more info on a command.')
            await ctx.send(embed=embed)

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot
        page = 0
        cogs = list(bot.cogs) # These cogs will be removed if they cannot run anything
        true_cogs = list(bot.cogs)  # get all of your cogs
        for cog in cogs:
            coga = bot.get_cog(cog)
            all_commands = [command for command in await self.filter_commands(coga.walk_commands(), sort=True)]
            if not all_commands:
                cogs.remove(cog)
        cmd = bot.get_command('jishaku')
        try:
            await cmd.can_run(ctx)
        except Exception as e:
            try:
                cogs.remove('Jishaku')
            except Exception as e:
                pass
        cogs.sort()

        def check(reaction, user):  # check who is reacting to the message
            return user == ctx.author
        embed = await self.bot_help_paginator(page, cogs)
        help_embed = await ctx.send(embed=embed)  # sends the first help page

        reactions = ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}',
                     '\N{BLACK LEFT-POINTING TRIANGLE}',
                     '\N{BLACK RIGHT-POINTING TRIANGLE}',
                     '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}',
                     '\N{BLACK SQUARE FOR STOP}',
                     '\N{INFORMATION SOURCE}')  # add reactions to the message
        bot.loop.create_task(self.bot_help_paginator_reactor(help_embed, reactions))
        # this allows the bot to carry on setting up the help command

        while 1:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)  # checks message reactions
            except TimeoutError:  # session has timed out
                try:
                    await help_embed.clear_reactions()
                except discord.errors.Forbidden:
                    pass
                break
            else:
                try:
                    await help_embed.remove_reaction(str(reaction.emoji), ctx.author)  # remove the reaction
                except discord.errors.Forbidden:
                    pass

                if str(reaction.emoji) == '⏭':  # go to the last the page
                    page = len(cogs) - 1
                    embed = await self.bot_help_paginator(page, cogs)
                    await help_embed.edit(embed=embed)
                elif str(reaction.emoji) == '⏮':  # go to the first page
                    page = 0
                    embed = await self.bot_help_paginator(page, cogs)
                    await help_embed.edit(embed=embed)

                elif str(reaction.emoji) == '◀':  # go to the previous page
                    page -= 1
                    if page == -1:  # check whether to go to the final page
                        page = len(cogs) - 1
                    embed = await self.bot_help_paginator(page, cogs)
                    await help_embed.edit(embed=embed)
                elif str(reaction.emoji) == '▶':  # go to the next page
                    page += 1
                    if page == len(cogs):  # check whether to go to the first page
                        page = 0
                    embed = await self.bot_help_paginator(page, cogs)
                    await help_embed.edit(embed=embed)

                elif str(reaction.emoji) == 'ℹ':  # show information help
                    all_cogs = '`, `'.join([cog for cog in cogs])
                    embed = discord.Embed(title=f'{bot.user.name} - Help', description=bot.description,
                                          color=discord.Colour.blue())
                    embed.set_thumbnail(url=ctx.bot.user.avatar_url)
                    embed.add_field(
                        name=f'There are {len(true_cogs)} cogs loaded :gear:.', #all cogs
                        value='`<...>` indicates a required argument,\n`[...]` indicates an optional argument.\n`╚╡` indicates a subcommand.\n\n'
                              '**Don\'t type these around your argument.**')
                    embed.add_field(name='Emoji key:',
                                    value=':track_previous: Goes to the first page\n'
                                          ':track_next: Goes to the last page\n'
                                          ':arrow_backward: Goes to the previous page\n'
                                          ':arrow_forward: Goes to the next page\n'
                                          ':stop_button: Deletes and closes this message\n'
                                          ':information_source: Shows this message')
                    embed.set_author(name=f'Suspended - page {page + 1}.')
                    embed.set_footer(text=f'Use "{self.clean_prefix}help <command>" for more info on a command.')
                    await help_embed.edit(embed=embed)

                elif str(reaction.emoji) == '⏹':  # delete the message and break from the wait_for
                    await help_embed.delete()
                    await ctx.message.add_reaction('✅') # Command run successfully
                    break

    async def bot_help_paginator_reactor(self, message, reactions):
        for reaction in reactions:
            await message.add_reaction(reaction)

    async def bot_help_paginator(self, page: int, cogs):
        ctx = self.context
        bot = ctx.bot
        cog = bot.get_cog(cogs[page])   # get the current cog
        all_commands = [command for command in await self.filter_commands(cog.walk_commands(), sort=True)] # filter the commands the user can use
        embed = discord.Embed(title=f'Help with {cog.qualified_name}',
                              description=cog.description, color=discord.Colour.blue())
        embed.set_author(name=f'Page {page + 1}')
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        for c in all_commands:
            if not c.hidden:
                signature = self.get_command_signature(c)
                description = self.get_command_description(c)
                if c.parent:  # it is a sub-command
                    embed.add_field(name=f'**╚╡**{signature}', value=description)
                else:
                    embed.add_field(name=signature, value=description, inline=False)
        embed.set_footer(text=f'Use "{self.clean_prefix}help <command>" for more info on a command.')
        return embed
