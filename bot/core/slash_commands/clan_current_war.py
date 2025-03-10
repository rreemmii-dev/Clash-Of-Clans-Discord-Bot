import coc
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from bot.functions import coc_timestamp_to_timestamp, create_embed, escape_markdown


async def clan_current_war(interaction: discord.Interaction, tag: str):
    try:
        clan_war = await Clash_of_clans.get_current_war(tag)
    except coc.errors.NotFound:
        await interaction.response.send_message(f"Clan not found\nThere is no clan with the tag `{tag}`.", ephemeral=True)
        return
    except coc.errors.PrivateWarLog:
        await interaction.response.send_message("Private war log\nThis clan has a private war log.", ephemeral=True)
        return
    if clan_war is None:
        await interaction.response.send_message("No war\nThis clan is not in a war", ephemeral=True)
        return
    text = f"{Emojis['members']} {clan_war.team_size} vs {clan_war.team_size}\n{Emojis['calendar']} {clan_war.state}: start{'ed' if clan_war.start_time.seconds_until < 0 else ''} <t:{coc_timestamp_to_timestamp(clan_war.start_time)}:R>, end{'ed' if clan_war.end_time.seconds_until < 0 else ''} <t:{coc_timestamp_to_timestamp(clan_war.end_time)}:R>"
    th_clan = {}
    th_opponent = {}
    for member in clan_war.members:
        if member.is_opponent:
            d = th_clan
        else:
            d = th_opponent
        if member.town_hall in d.keys():
            d[member.town_hall] += 1
        else:
            d[member.town_hall] = 1
    text += "\nClan roaster:\n"
    for th in sorted(th_clan.keys(), reverse=True):
        text += f"{Emojis['th_emojis'][th]} {th_clan[th]} "
    text += "\nOpponent roaster:\n"
    for th in sorted(th_opponent.keys(), reverse=True):
        text += f"{Emojis['th_emojis'][th]} {th_opponent[th]} "
    embed = create_embed(f"Clan war: {escape_markdown(clan_war.clan.name)} ({clan_war.clan.tag}) :crossed_swords: {escape_markdown(clan_war.opponent.name)} ({clan_war.opponent.tag})", text, interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
