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
bot = commands.Bot(command_prefix='c')
bot.launch_time = datetime.utcnow()


initial_extensions = ['Cogs.Admin', 'Cogs.Fun', 'Cogs.Utility', 'Cogs.Error']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
bot.load_extension('jishaku')

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
