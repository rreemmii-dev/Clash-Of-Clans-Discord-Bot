import coc
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.functions import create_embed, escape_markdown
from data.views import ComponentView


async def clan_super_troops_activated_embed(interaction: discord.Interaction, clan_tag: str, super_troop: str) -> discord.Embed:
    clan = await Clash_of_clans.get_clan(clan_tag)
    members_with_super_troop = []
    max_level = "Max level unknown"
    async for member in clan.get_detailed_members():
        s_troop = member.get_troop(super_troop)
        if s_troop is not None and s_troop.is_active:
            normal_troop = member.get_troop(s_troop.original_troop.name, is_home_troop=True)
            max_level = normal_troop.max_level
            level = normal_troop.level
            members_with_super_troop.append({"name": member.name, "tag": member.tag, "super_troop_level": level})
    text = ""
    for player in members_with_super_troop:
        text += f"{escape_markdown(player['name'])}: {super_troop} level {player['super_troop_level']}/{max_level} | {player['tag']}\n"
    if text == "":
        text = f"No player has the {super_troop} active in this clan"
    embed = create_embed(f"Members with the {super_troop} active in the clan {escape_markdown(clan.name)} ({clan.tag})", text, interaction.guild.me.color, f"clan_super_troops_activated|{interaction.user.id}", icon_url=interaction.guild.me.display_avatar.url)
    return embed


async def clan_super_troops_activated(interaction: discord.Interaction, clan_tag: str, super_troop: str):
    try:
        await Clash_of_clans.get_clan(clan_tag)
    except coc.errors.NotFound:
        await interaction.response.send_message(f"Clan not found\nThere is no clan with the tag `{clan_tag}`.", ephemeral=True)
        return
    embed = await clan_super_troops_activated_embed(interaction, clan_tag, super_troop)

    await interaction.response.send_message(embed=embed, view=ComponentView("clan_super_troops_activated"))
    return
