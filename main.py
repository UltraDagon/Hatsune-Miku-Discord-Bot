# Base libraries
import os
import discord
import asyncio
import dotenv
from keep_alive import keep_alive

import random
import datetime, pytz
from termcolor import colored

client = discord.Client()


# :Keep at top

class Bot:
    fill = 1


@client.event
async def status_task():
    while True:
        await asyncio.sleep(60)


@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print(colored(("Ready at " + str(datetime.datetime.now(pytz.timezone("US/Central")))[:-13] + "\n\n"), "cyan",
                  attrs=['bold']))


@client.event
async def on_message(msg):
    # Puts discord message into console
    print("\n\n" + str(datetime.datetime.now(pytz.timezone("US/Central")))[:-13] + " - " + str(
        msg.author) + " in [" + str(msg.guild) + "] - #" + str(msg.channel) + ":")
    print(msg.content)

    if client.user == msg.author:
        return

    if msg.content[0] == '%':
        cmd = str(msg.content)[1:].lower().splitlines()

        if cmd[0] in ["hello", "hi"]:
            await msg.channel.send("Hello!")

# Keep this at the end
keep_alive()
token = os.environ.get('DISCORD_BOT_SECRET')
client.run(token)