import discord

from bot.functions import escape_markdown
from data.useful import Ids


async def guild_remove(self: discord.AutoShardedClient, guild: discord.Guild):
    users = 0
    bots = 0
    for member in await guild.chunk(cache=False):
        if member.bot:
            bots += 1
        else:
            users += 1
    if users >= 100:
        log = self.get_channel(Ids["guilds_bot_log_channel"])
        await log.send(f"The bot has LEFT the server {escape_markdown(guild.name)},\n owned by {escape_markdown(guild.owner.name)},\n with {users + bots} members ({users} users and {bots} bots)")
    nb_guilds = len(self.guilds)
    act = discord.Activity(type=discord.ActivityType.watching, name=f"{nb_guilds: ,} servers")
    await self.change_presence(status=discord.Status.online, activity=act)
    return
