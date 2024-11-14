import discord

from bot.functions import escape_markdown


async def find_user_by_id(interaction: discord.Interaction, user_id: int):
    user = await interaction.client.fetch_user(user_id)
    if user is not None:
        await interaction.response.send_message(f"{escape_markdown(user.name)}#{user.discriminator} {user.mention}")
    else:
        await interaction.response.send_message("This user has not common servers with Clash INFO.")
    return
