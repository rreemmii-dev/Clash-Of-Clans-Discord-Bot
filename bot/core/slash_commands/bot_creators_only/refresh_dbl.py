import discord

from bot.emojis import Emojis
from data.config import Config
from data.useful import Ids


async def refresh_dbl(interaction: discord.Interaction):
    if Config["top_gg"]:
        from bot.apis_clients.top_gg import Dbl_client
        await Dbl_client.post_guild_count(guild_count=len(interaction.client.guilds))
        await interaction.response.send_message(f"{Emojis['Yes']} Done: https://top.gg/bot/{Ids['Bot']}")
    else:
        await interaction.response.send_message("Top.gg has been disabled from `config.json`")
    return
