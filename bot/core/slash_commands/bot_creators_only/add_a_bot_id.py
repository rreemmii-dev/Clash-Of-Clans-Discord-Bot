import discord

from bot.functions import create_embed


async def add_a_bot_id(interaction: discord.Interaction, bot_id: int):
    link = discord.utils.oauth_url(bot_id, permissions=discord.Permissions(administrator=True))
    embed = create_embed(f"Add the bot with the ID {bot_id}:", link, interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
