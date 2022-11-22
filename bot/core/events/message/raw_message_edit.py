import discord

from data.config import Config


async def raw_message_edit(self: discord.AutoShardedClient, payload: discord.RawMessageUpdateEvent):
    if not Config["message_content_intent"]:
        return

    return
