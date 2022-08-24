import discord

from bot.core.slash_commands.buildings_bh import buildings_bh_embed


async def change_bh_lvl(interaction: discord.Interaction):
    embed = await buildings_bh_embed(interaction, int(interaction.data["values"][0]))
    await interaction.response.edit_message(embed=embed)
    return
