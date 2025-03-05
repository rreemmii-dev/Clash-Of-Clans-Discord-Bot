import discord

from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown
from data.useful import Ids
from data.views import ComponentView


async def guild_join(self: discord.AutoShardedClient, guild: discord.Guild):
    users = 0
    bots = 0
    for member in await guild.chunk(cache=False):
        if member.bot:
            bots += 1
        else:
            users += 1
    if users >= 100:
        log = self.get_channel(Ids["guilds_bot_log_channel"])
        await log.send(f"The bot has JOINED the server {escape_markdown(guild.name)},\n owned by {escape_markdown(guild.owner.name)},\n with {users + bots} members ({users} users and {bots} bots)")

    nb_guilds = len(self.guilds)
    act = discord.Activity(type=discord.ActivityType.watching, name=f"{nb_guilds: ,} servers")
    await self.change_presence(status=discord.Status.online, activity=act)

    channel_created = False
    for channel in guild.text_channels:
        if "clash-info-news" in channel.name:
            if channel.permissions_for(guild.me) >= discord.Permissions(embed_links=True, external_emojis=True, send_messages=True, view_channel=True):
                channel_created = True
                break
    else:
        if guild.me.guild_permissions.manage_channels and guild.me.guild_permissions.manage_roles:
            if discord.Permissions(embed_links=True, external_emojis=True, send_messages=True, view_channel=True) <= guild.me.guild_permissions:
                overwrite = {guild.default_role: discord.PermissionOverwrite(view_channel=True, send_messages=False), guild.me: discord.PermissionOverwrite(embed_links=True, external_emojis=True, send_messages=True, view_channel=True)}
                channel = await guild.create_text_channel("clash-info-news", overwrites=overwrite)
                channel_created = True
    if channel_created:
        embed = create_embed("Thanks for using this bot on your server !", f"Hello\n\nIf you want to receive news about the bot, please hit the button {Emojis['news']} bellow. If you want to delete this channel, please hit the button {Emojis['Delete']} bellow.\n\nYou can see all useful links in the bot About Me section.", 0x00ffff, "joined_guild_message", guild.me.display_avatar.url)
        await channel.send(embed=embed, view=ComponentView("joined_guild_message"))
        await channel.send("https://discord.gg/KQmstPw")
    return
