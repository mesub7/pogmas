import discord
from discord.ext import tasks, commands
import logging
import time
from datetime import datetime
from random import randint

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Just before starting

print('------')
print('Attempting to connect to discord...')

# The other sutff

token = open("tokendev.txt","r").readline()
bot = commands.Bot(command_prefix='p')
bot.launch_time = datetime.utcnow()

@bot.command(description='Pings the bot.')
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send("Ping...")
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content='Pong! {:.2f}ms'.format(duration))

@bot.command(description='Some info about the bot.')
async def about(ctx):
    embed = discord.Embed(title="Pogmas", colour=discord.Colour(0x38fe), description="A simple discord bot for Transport Dash, built and maintained by mesub#0556.")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/740568208351690803/54fff7b36442635ac6bfd3f457cec28a.png")
    embed.set_footer(text="mesub#0556", icon_url="https://cdn.discordapp.com/embed/avatars/414530505585721357.png")
    embed.add_field(name="About", value="This is just a simple bot to make some tasks in Transport Dash a little easier. Don't expect much Functionality outside of it 😄.")
    embed.add_field(name="Source code", value="If you want to play around with the bot or run an instance of it, then the code can be found [here](https://github.com/mesub7/pogmas)")
    await ctx.send(embed=embed)

@bot.command(hidden=True)
async def restart(ctx):
    bot_owner_id = 414530505585721357
    restart = True
    if ctx.author.id == bot_owner_id:
        message = await ctx.send("Ok! I'll restart now...")
        await bot.close()
    else:
        await ctx.send("You don't need to use this command :)")

@bot.command(hidden=True)
@commands.has_any_role(407585313129758720, 521372852952498179)
async def say(ctx, channel:discord.TextChannel, *, words:str):
        channel = channel
        await channel.send(words)

# If they don't have a role for it
@say.error
async def say_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingAnyRole):
        await ctx.send("You cannot run this command as you don't have the role required.")

@bot.command(description="Produces a random number from 1!")
async def random(ctx, limit):
    result = randint(1, int(limit))
    await ctx.send("The result is: %s!" % result)

@bot.command(description="See how long the bot has been online for!")
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"I have been up for: {days}d, {hours}h, {minutes}m, and {seconds}s")

# This adds reactions to the changelog channel
@bot.event
async def on_message(message):
    channel = 703665588244971582
    emoji = '\N{THUMBS UP SIGN}'
    emoji1 = '\N{THUMBS DOWN SIGN}'
    if channel == int(message.channel.id):
        await message.add_reaction(emoji)
        await message.add_reaction(emoji1)
    await bot.process_commands(message)

# Reminding myself about Question of the day
@tasks.loop(hours=168)
async def questioner():
    channel = bot.get_channel(526817279476891648)
    await bot.send('<@414530505585721357> Make sure you add the react with something for a chance to be questioner.')

@tasks.loop(hours=168)
async def questioner_a():
    channel = bot.get_channel(526817279476891648)
    await bot.send('<@414530505585721357> Make sure that you pick a questioner.')

@questioner.before_loop
async def on_saturday():
    time = datetime.utcnow()
    await discord.utils.sleep_until(date.weekday(6))


@questioner_a.before_loop
async def on_sunday():
    await discord.utils.sleep_until(date.weekday(0))

questioner.start()
questioner_a.start()

@bot.event
async def on_ready():
    print('------')
    print('Connected!')
    print('Logged on as' + ' ' + str(bot.user))
    print('User ID is:' + ' ' + str (bot.user.id))
    print('------')
    activity = discord.Activity(name='mesub breathe life into me by adding code. Experimental.', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)


bot.run(token)
