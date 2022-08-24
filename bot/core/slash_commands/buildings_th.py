import discord

from bot.functions import create_embed
from data.clash_of_clans import Main_base_buildings
from data.useful import Useful
from data.views import ComponentView


async def buildings_th_embed(interaction: discord.Interaction, lvl: int) -> discord.Embed:
    level_th = Main_base_buildings[lvl]
    text_th = ""
    for category, buildings in level_th.items():
        text_th += f"\n__{category}:__\n"
        for building_name, building_max_level in buildings.items():
            text_th += f"{building_name} max level: {building_max_level}\n"
    embed = create_embed(f"__**TH {lvl}:\n**__", text_th, interaction.guild.me.color, f"buildings_th|{interaction.user.id}", interaction.guild.me.display_avatar.url)
    return embed


async def buildings_th(interaction: discord.Interaction, lvl: int):
    if lvl > Useful["max_th_lvl"] or lvl < 0:
        await interaction.response.send_message(f"Town Hall not found\nPlease give a valid TH level: there is no level `{lvl}` TH.", ephemeral=True)
        return

    elif lvl == 0:
        embed = create_embed("What is your TH level ?", "", interaction.guild.me.color, f"buildings_th|{interaction.user.id}", interaction.guild.me.display_avatar.url)
        await interaction.response.send_message(embed=embed, view=ComponentView("buildings_th"))

    elif 0 < lvl <= Useful["max_th_lvl"]:
        embed = await buildings_th_embed(interaction, lvl)
        await interaction.response.send_message(embed=embed, view=ComponentView("buildings_th"))
    return
