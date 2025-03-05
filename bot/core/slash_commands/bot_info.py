import discord

from bot.apis_clients.discord import Clash_info
from bot.emojis import Emojis
from bot.functions import create_embed
from data.useful import Useful


async def bot_info(interaction: discord.Interaction):
    required_permissions = Useful["required_permissions"]
    text_permissions = ":warning: The bot needs the permissions: "
    for perm in required_permissions:
        if not getattr(interaction.app_permissions, perm):
            text_permissions += "\n" + perm
    text_permissions += "\nSo please grant them to the bot."
    if text_permissions == ":warning: The bot needs the permissions: " + "\nSo please grant them to the bot.":
        text_permissions = f"{Emojis['yes']} The bot has all required permissions !"
    text_servers_number = f"{Emojis['discord']} The bot is on {len(Clash_info.guilds)} servers !"
    text_created = f"{Emojis['calendar']} The bot was created the 2020-04-28, and certified the 2020-09-23."
    embed = create_embed("Clash INFO", f"{text_permissions}\n{text_servers_number}\n{text_created}", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
