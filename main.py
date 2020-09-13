# Base libraries
import os
import sys
import discord
import asyncio
import aiohttp
import lavalink
import psutil
from io import BytesIO
from keep_alive import keep_alive
from discord.ext import commands
from discord import utils

import random
import datetime, pytz
from termcolor import colored

bot = commands.Bot(command_prefix='%')
client = bot


# :Keep at top


async def get_image(image):
    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            data = BytesIO(await resp.read())
            return data


@client.event
async def status_task():
    while True:
        await asyncio.sleep(60)


@client.event
async def on_ready():
    client.loop.create_task(status_task())
    print(sys.version)
    print(colored(("Ready at " + str(datetime.datetime.now(pytz.timezone("US/Central")))[:-13] + "\n\n"), "cyan", attrs=['bold']))


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
        await client
        await client.close()
        print(colored("\n\nBot was force stopped.\n\n", "red", attrs=['bold']))


@bot.command(name='hello', aliases=['hi'])
async def hello(msg):
    await msg.channel.send("Hello!", file=discord.File(await get_image("https://hatsunemiku-bot.weebly.com/uploads/4/6/4/8/46482037/waving_orig.png"), "waving.png"))


MusicBot = bot
MusicBot.music = lavalink.Client(754169016087478302)  # Bot's user id
MusicBot.music.add_node("localhost", 80, "ILoveHatsuneMiku", "na", "music-node")
MusicBot.add_listener(MusicBot.music.voice_update_handler, "on_socket_response")


@bot.command(name='join')
async def join(ctx):
    print('join command worked')
    try:
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            print(vc)
            player = MusicBot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await connect_to(ctx.guild.id, str(vc.id))
    except():
        await ctx.channel.send("Uh oh! There was an error joining the voice channel! This is most likely due the bot being run on Heroku, which doesn't support music bots. All other commands will work.")


async def track_hook(event):
    if isinstance(event, lavalink.events.QueueEndEvent):
        guild_id = int(event.player.guild_id)
        await connect_to(guild_id, None)


async def connect_to(guild_id: int, channel_id: str):
    """ Connects to a given voice channel ID. A channel_id of 'None' means disconnected"""
    ws = MusicBot._connection._get_websocket(guild_id)
    await ws.voice_state(str(guild_id), channel_id)

# Keep this at the end
keep_alive()
token = os.environ.get('DISCORD_BOT_SECRET')
client.run(token)
