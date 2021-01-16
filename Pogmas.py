import discord
from discord.ext import tasks, commands
import logging
from datetime import datetime
import Cogs.Help as h

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def load_ids():
    bot.no_cut = []
    with open('no_cut.txt') as file:
        for line in file:
            line = line.rstrip('\n')
            try:
                bot.no_cut.append(int(line))
            except Exception as e:
                pass

# Just before starting

print('------')
print('Attempting to connect to discord...')

# The other sutff
intents = discord.Intents.default()
intents.members = True

token = open("token.txt","r").readline()

bot = commands.Bot(command_prefix='p',status=discord.Status.online, actvity=discord.Activity(type=discord.ActivityType.watching, name="JoshiWoshi04's videos."), \
intents=intents, help_command=h.PogmasHelpCommand())
bot.launch_time = datetime.utcnow()
bot.owner_id = 414530505585721357

bot.initial_extensions = ['Cogs.Admin', 'Cogs.Fun', 'Cogs.Utility', 'Cogs.Error', 'Cogs.TD']

if __name__ == '__main__':
    for extension in bot.initial_extensions:
        bot.load_extension(extension)
bot.load_extension('jishaku')

load_ids()
cmd = bot.get_command('jishaku py')
cmd.aliases.append('eval')
# register the modified command
bot.remove_command('jishaku py')
bot.add_command(cmd)

@bot.event
async def on_ready():
    print('------')
    print('Connected!')
    print('Logged on as' + ' ' + str(bot.user))
    print('User ID is:' + ' ' + str (bot.user.id))
    print('------')

@bot.check
async def no_dms(ctx):
    return ctx.guild is not None

bot.run(token)
