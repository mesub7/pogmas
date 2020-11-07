import discord
from discord.ext import commands



def lvl3():
    def predicate(ctx):
        role = discord.Role
        return any(
        role.id in [770380094866063380, 660926272750223361, 754287737439387679, 407585313129758720, 521372852952498179]
        for role in ctx.author.roles
        ) or ctx.author.id == 414530505585721357
    return commands.check(predicate)

async def lvl4(ctx):
    return ctx.author.id in (252504297772679168, 378924582452723734, 325357652752203777, 240035755458691072,\
    439784355343237151, 290619509641838603, 390978899645038602, 414530505585721357, 197100324727685121)
