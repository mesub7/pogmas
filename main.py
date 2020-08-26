import discord
from discord.ext import commands
import logging
import time

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = open("token.txt","r").readline()
bot = commands.Bot(command_prefix='p')

@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send("Ping...")
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content='Pong! {:.2f}ms'.format(duration))
    

@bot.event
async def on_message(message):
    channel = 703665588244971582
    emoji = '\N{THUMBS UP SIGN}'
    emoji1 = '\N{THUMBS DOWN SIGN}'
    if channel == int(message.channel.id):
        await message.add_reaction(emoji)
        await message.add_reaction(emoji1)
    await bot.process_commands(message)
        

@bot.event
async def on_ready():
    print('------')
    print('Logged on as' + ' ' + str(bot.user))
    print('User ID is:' + ' ' + str (bot.user.id))
    print('------')
    activity = discord.Activity(name='Golden Squid\'s & AlphaZulu\'s videos. Proudly powered by GCP. I blush because I am cuute', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)


bot.run(token)
