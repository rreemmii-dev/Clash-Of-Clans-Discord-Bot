import discord


from bot.core.events.ready.ready import ready

from bot.core.events.guild.guild_join import guild_join
from bot.core.events.guild.guild_remove import guild_remove

from bot.core.events.member.member_join import member_join
from bot.core.events.member.member_remove import member_remove

from bot.core.events.message.raw_message_edit import raw_message_edit
from bot.core.events.message.message import on_message


class Bot(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents, chunk_guilds_at_startup=False)
        self.id = None

    async def sync_commands(self):
        pass

    async def on_ready(self):
        await ready(self)

    async def on_guild_join(self, guild: discord.Guild):
        await guild_join(self, guild)
        return

    async def on_guild_remove(self, guild: discord.Guild):
        await guild_remove(self, guild)
        return

    async def on_member_join(self, member: discord.Member):
        await member_join(self, member)
        return

    async def on_member_remove(self, member: discord.Member):
        await member_remove(self, member)
        return

    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        await raw_message_edit(self, payload)
        return

    async def on_message(self, message: discord.Message):
        await on_message(self, message)
        return
