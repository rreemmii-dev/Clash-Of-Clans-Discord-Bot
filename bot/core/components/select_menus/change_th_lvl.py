import discord

from bot.core.slash_commands.buildings_th import buildings_th_embed


async def change_th_lvl(interaction: discord.Interaction):
    embed = await buildings_th_embed(interaction, int(interaction.data["values"][0]))
    await interaction.response.edit_message(embed=embed)
    return
