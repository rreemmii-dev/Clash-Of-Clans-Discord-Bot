import discord

from bot.core.slash_commands.clan_super_troops_activated import clan_super_troops_activated_embed


async def change_clan_super_troops_activated(interaction: discord.Interaction):
    clan_tag = f"#{interaction.message.embeds[0].title.split('#')[-1].split('(')[0].split(')')[0]}"
    super_troop = interaction.data["values"][0]
    embed = await clan_super_troops_activated_embed(interaction, clan_tag, super_troop)
    await interaction.response.edit_message(embed=embed)
    return
