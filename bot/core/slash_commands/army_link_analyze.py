import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from bot.functions import create_embed


async def army_link_analyze(interaction: discord.interactions, army_link: str):
    troops, spells = Clash_of_clans.parse_army_link(army_link)
    text = f"[This army]({army_link}) contains:\n\n"
    if [troops, spells] != [[], []]:
        for troop, quantity in troops:
            text += f"{quantity} {Emojis['Troops_emojis'][troop.name]} ({troop.name})\n"
        for spell, quantity in spells:
            text += f"{quantity} {Emojis['Troops_emojis'][spell.name]} ({spell.name})\n"
    else:
        text += "Nothing! Make sure your link is really an army link"
    embed = create_embed(f"Analyze of the in-game army link", text, interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
