import discord
import aiohttp
from io import BytesIO
from discord.ext import commands
from discord import utils


async def get_image(image):
    async with aiohttp.ClientSession() as session:
        async with session.get(image) as resp:
            data = BytesIO(await resp.read())
            return data

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', aliases=['hi'])
    async def hello(self, msg):
        await msg.channel.send("Hello!", file=discord.File(await get_image("https://hatsunemiku-bot.weebly.com/uploads/4/6/4/8/46482037/waving_orig.png"), "waving.png"))

def setup(bot):
    bot.add_cog(FunCog(bot))