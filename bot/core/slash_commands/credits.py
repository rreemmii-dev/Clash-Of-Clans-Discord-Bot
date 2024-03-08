import discord

from bot.emojis import Emojis
from bot.functions import create_embed
from data.useful import Ids


async def credits(interaction: discord.Interaction):
    text = ""

    text += "**Bot creators:**\n"
    for creator_id in Ids["Creators"]:
        text += f"<@{creator_id}>\n"

    text += "\n\n**Python libraries used:**\n"
    text += "[discord.py](https://github.com/Rapptz/discord.py)\n"
    text += "[coc.py](https://github.com/mathsman5133/coc.py)\n"

    text += "\n\n**Patreon subscribers:**\n"
    text += "\nPlatinum:\n*Nobody*\n"
    text += "\nGold:\n*Nobody*\n"
    text += "\nBronze:\n*Nobody*\n"
    text += f"\nIf you want to join them, please consider subscribing to our [{Emojis['Patreon']} Patreon](https://www.patreon.com/clash_info)"

    embed = create_embed("Credits", text, interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
