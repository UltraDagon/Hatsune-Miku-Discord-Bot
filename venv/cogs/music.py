from discord.ext import commands
from discord import utils
import lavalink

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(754169016087478302)  # Bot's user id
        self.bot.music.add_node("localhost", 7000, "ILoveHatsuneMiku", "na", "music-node")
        self.bot.add_listener(self.bot.music.voice_update_handler, "on_socket_response")
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command(name='join')
    async def join(self, ctx):
        print('join command worked')
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to a given voice channel ID. A channel_id of 'None' means disconnected"""
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

def setup(bot):
    bot.add_cog(MusicCog(bot))