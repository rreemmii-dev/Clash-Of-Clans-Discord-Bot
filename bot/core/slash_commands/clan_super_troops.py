import coc
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown


async def clan_super_troops(interaction: discord.Interaction, clan_tag: str):
    try:
        clan = await Clash_of_clans.get_clan(clan_tag)
    except coc.errors.NotFound:
        await interaction.response.send_message(f"Clan not found\nThere is no clan with the tag `{clan_tag}`.", ephemeral=True)
        return
    super_troops = {}
    super_troops_max_level = {}
    for s_troop in coc.SUPER_TROOP_ORDER:
        super_troops[s_troop] = []
        super_troops_max_level[s_troop] = -1
    async for member in clan.get_detailed_members():
        for s_troop in member.super_troops:
            if s_troop.is_active:
                normal_troop = member.get_troop(s_troop.original_troop.name, is_home_troop=True)
                super_troops_max_level[s_troop.name] = normal_troop.max_level
                level = normal_troop.level
                super_troops[s_troop.name].append({"name": member.name, "tag": member.tag, "super_troop_level": level})
    text = ""
    for super_troop_name, players in super_troops.items():
        players.sort(key=lambda p: p['super_troop_level'], reverse=True)
        text += f"**{Emojis['Troops_emojis'][super_troop_name]} {super_troop_name}**:\n"
        for player in players:
            text += f"level {player['super_troop_level']}/{super_troops_max_level[super_troop_name]}: {escape_markdown(player['name'])} ({player['tag']})\n"
        text += "\n"
    if text == "":
        text = f"No super troop has been activated by any player in this clan"
    embed = create_embed(f"Super troops activated by members of the clan {escape_markdown(clan.name)} ({clan.tag})", text, interaction.guild.me.color, f"clan_super_troops|{interaction.user.id}", icon_url=interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
