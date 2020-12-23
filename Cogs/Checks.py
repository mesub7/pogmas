import discord
from discord.ext import commands

"""
Level 1 - Everyone
Level 2 - Transport Dash Premium
Level 3 - Transport Dash Staff
Level 4 - Upper Staff
Level 5 - Bot Dev & Trusted User
"""

async def lvl2(ctx):
        role = discord.Role
        return any(
        role.id in [660926272750223361, 754287737439387679, 407585313129758720, 521372852952498179, 481034890792534018] #Transport Booster, YT member, Owner, Server Manager, staff respectivly
        for role in ctx.author.roles
        ) or await lvl5(ctx) #TD Premium, Me or Trusted user

async def lvl3(ctx):
    role = discord.Role
    return any(
    role.id in [481034890792534018]
    for role in ctx.author.roles
    ) or await lvl5(ctx)  #Staff or me/Trusted user

async def lvl4(ctx):
    return ctx.author.id in (252504297772679168, 378924582452723734, 325357652752203777, 240035755458691072,\
    439784355343237151, 290619509641838603, 390978899645038602, 414530505585721357, 197100324727685121, 555459418591068170, 197100324727685121) #People in a specific channel / Trusted user

async def lvl5(ctx):
    return ctx.author.id in (414530505585721357, 197100324727685121) #Me or trusted user only
