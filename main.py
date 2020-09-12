# Base libraries
import os
import sys
import discord
import asyncio
from keep_alive import keep_alive
from discord.ext import commands

import random
import datetime, pytz
from termcolor import colored

bot = commands.Bot(command_prefix='%')
client = bot


# :Keep at top


@client.event
async def status_task():
    while True:
        await asyncio.sleep(60)


@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print(sys.version)
    print(colored(("Ready at " + str(datetime.datetime.now(pytz.timezone("US/Central")))[:-13] + "\n\n"), "cyan",
                  attrs=['bold']))

    bot.load_extension('cogs.music')
    bot.load_extension('cogs.fun')


@client.event
async def on_message(msg):
    await bot.process_commands(msg)
    # Puts discord message into console
    print("\n\n" + str(datetime.datetime.now(pytz.timezone("US/Central")))[:-13] + " - " + str(
        msg.author) + " in [" + str(msg.guild) + "] - #" + str(msg.channel) + ":")
    print(msg.content)

    if client.user == msg.author:
        return

    if msg.author.id == 254364268789628938 and msg.content == ">%forcestop":
        await client.close()
        print(colored("\n\nBot was force stopped.\n\n", "red", attrs=['bold']))

# Keep this at the end
keep_alive()
token = os.environ.get('DISCORD_BOT_SECRET')
client.run(token)