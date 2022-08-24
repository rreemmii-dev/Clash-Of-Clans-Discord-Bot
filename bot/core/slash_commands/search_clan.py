import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.core.slash_commands.clan_info import clan_info_embed
from bot.functions import escape_markdown


async def search_clan(interaction: discord.Interaction, name: str):
    if len(name) < 3:
        await interaction.response.send_message(f"Clan name has to be at least 3 characters long, not `{name}`")
        return
    clans = await Clash_of_clans.search_clans(name=name, limit=25)
    if not clans:
        await interaction.response.send_message(f"There is no clan with the name `{name}`")
        return

    first_embed_defined = False

    select = discord.ui.Select(placeholder="Select your clan", min_values=1, max_values=1)
    for clan in clans:
        if not first_embed_defined:
            embed = await clan_info_embed(interaction, clan.tag)
            embed.set_footer(text=f"search_clan|{interaction.user.id}")
            first_embed_defined = True
        select.add_option(label=f"{escape_markdown(clan.name)} ({clan.tag}) - Level {clan.level}", value=clan.tag)

    await interaction.response.send_message(embed=embed, view=discord.ui.View(timeout=None).add_item(select))
    return
