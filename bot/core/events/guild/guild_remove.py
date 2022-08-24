import discord

from bot.functions import escape_markdown
from data.config import Config
from data.useful import Ids


async def guild_remove(self: discord.Client, guild: discord.Guild):
    if Config["top_gg"]:
        from bot.apis_clients.top_gg import Dbl_client
        await Dbl_client.post_guild_count(guild_count=len(self.guilds))

    users = 0
    bots = 0
    for member in guild.members:
        if member.bot:
            bots += 1
        else:
            users += 1
    if users >= 100:
        log = self.get_channel(Ids["Guilds_bot_log_channel"])
        await log.send(f"The bot has LEFT the server {escape_markdown(guild.name)},\n owned by {escape_markdown(guild.owner.name)},\n with {len(guild.members)} members ({users} users and {bots} bots)")
    nb_guilds = len(self.guilds)
    act = discord.Activity(type=discord.ActivityType.watching, name=f"{nb_guilds: ,} servers")
    await self.change_presence(status=discord.Status.online, activity=act)
    return
