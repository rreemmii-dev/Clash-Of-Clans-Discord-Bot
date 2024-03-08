import discord

from bot.functions import create_embed
from data.clash_of_clans import Builder_base_buildings
from data.useful import Useful
from data.views import ComponentView


async def buildings_bh_embed(interaction: discord.Interaction, lvl: int) -> discord.Embed:
    level_bh = Builder_base_buildings[lvl]
    text_bh = ""
    for category, buildings in level_bh.items():
        text_bh += f"\n__{category}:__\n"
        for building_name, building_max_level in buildings.items():
            text_bh += f"{building_name}: {building_max_level}\n"
    embed = create_embed(f"__**Buildings max level (BH {lvl}):\n**__", text_bh, interaction.guild.me.color, f"buildings_bh|{interaction.user.id}", interaction.guild.me.display_avatar.url)
    return embed


async def buildings_bh(interaction: discord.Interaction, lvl: int):
    if lvl > Useful["max_bh_lvl"] or lvl < 0:
        await interaction.response.send_message(f"Builder Hall not found\nPlease give a valid BH level: there is no level `{lvl}` BH.", ephemeral=True)
        return

    elif lvl == 0:
        embed = create_embed("What is your BH level ?", "", interaction.guild.me.color, f"buildings_bh|{interaction.user.id}", interaction.guild.me.display_avatar.url)
        await interaction.response.send_message(embed=embed, view=ComponentView("buildings_bh"))

    elif 0 < lvl <= Useful["max_bh_lvl"]:
        embed = await buildings_bh_embed(interaction, lvl)
        await interaction.response.send_message(embed=embed, view=ComponentView("buildings_bh"))
    return
