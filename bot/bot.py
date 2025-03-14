import discord


from bot.core.events.ready.ready import ready

from bot.core.events.guild.guild_join import guild_join
from bot.core.events.guild.guild_remove import guild_remove

from bot.core.events.message.message import on_message


class Bot(discord.AutoShardedClient):
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

    async def on_message(self, message: discord.Message):
        await on_message(self, message)
        return
