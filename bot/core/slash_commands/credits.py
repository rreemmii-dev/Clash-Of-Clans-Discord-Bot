import discord

from bot.functions import create_embed
from data.useful import Ids


async def credits(interaction: discord.Interaction):
    text = ""

    text += "**Bot creators:**\n"
    for creator_id in Ids["creators"]:
        text += f"<@{creator_id}>\n"
    text += "\n\n**Python libraries used:**\n"
    text += "[discord.py](https://github.com/Rapptz/discord.py)\n"
    text += "[coc.py](https://github.com/mathsman5133/coc.py)\n"

    embed = create_embed("Credits", text, interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
