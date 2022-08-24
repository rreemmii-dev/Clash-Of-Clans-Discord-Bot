import discord

from bot.core.slash_commands.clan_info import clan_info_embed


async def change_search_clan(interaction: discord.Interaction):
    embed = await clan_info_embed(interaction, interaction.data["values"][0])
    embed.set_footer(text=f"search_clan|{interaction.user.id}")
    await interaction.response.edit_message(embed=embed)
    return
