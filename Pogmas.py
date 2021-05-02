import discord
from discord.ext import commands
import logging
from datetime import datetime
import Cogs.Help as h
import asyncio
import aiosqlite
import os


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


async def load_ids():
    bot.no_cut=[]
    print('Loading IDs from database.')
    bot.db.row_factory = aiosqlite.Row
    query = await bot.db.execute('SELECT * FROM cuts')
    rows = await query.fetchall()
    for row in rows:
        bot.no_cut.append(int(f"{row['id']}"))
    print('IDs loaded!')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "Pogmas.db")
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'true'

async def db_connect():
    print('------')
    print('Connecting to databse...')
    return await aiosqlite.connect(db_path)

def run_bot():
    bot.db = bot.loop.run_until_complete(db_connect())
    if bot.db is not None:
            print('Connected to database!')
            print('------')
    bot.loop.run_until_complete(load_ids())
    print('------')
    print('Attempting to connect to discord...')
    bot.run(token)


# The other stuff

token = open('token.txt','r').readline()
role = discord.Role

intents = discord.Intents.default()
intents.members = True
mentions = discord.AllowedMentions()
mentions.everyone = False
mentions.users = True
mentions.roles = [discord.Object(id=790631558976503830)]
mentions.replied_user = True

bot = commands.Bot(help_command=h.PogmasHelpCommand(), intents=intents,
command_prefix='p',status=discord.Status.online, allowed_mentions=mentions)

bot.launch_time = datetime.utcnow()
bot.owner_id = 414530505585721357
bot.initial_extensions = ['Cogs.Admin', 'Cogs.Fun', 'Cogs.Utility', 'Cogs.Error', 'Cogs.TD']

if __name__ == '__main__':
    for extension in bot.initial_extensions:
        bot.load_extension(extension)


bot.load_extension('jishaku')
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

run_bot()
