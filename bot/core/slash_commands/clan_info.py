import coc
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown


async def clan_info_embed(interaction: discord.Interaction, tag: str) -> discord.Embed:
    clan = await Clash_of_clans.get_clan(tag)
    if clan.location is not None:
        location = clan.location.name
    else:
        location = "International"
    leader = "None"
    for member in clan.members:
        if member.role is coc.Role.leader:
            leader = member
            break
    if clan.public_war_log:
        wars_data = f"{clan.war_wins} wins, {clan.war_ties} ties and {clan.war_losses} losses"
    else:
        wars_data = f"{clan.war_wins} wins (private war log)"
    embed = create_embed(f"Clan: {escape_markdown(clan.name)} ({clan.tag})", f"{Emojis['Trophy']} Clan points: {clan.points: ,}\n{Emojis['Versus_trophy']} Builder base clan points: {clan.builder_base_points: ,}\n{Emojis['War_leagues'][clan.war_league.name]} League: {clan.war_league}\n{Emojis['Trophy']} Required trophies: {clan.required_trophies: ,}\n{Emojis['Owner']} Leader: {escape_markdown(leader.name)} ({leader.tag})\n{Emojis['Members']} Number of members: {clan.member_count}\n:crossed_swords: Wars: {wars_data}\n{Emojis['Pin']} Location: {location}\n{Emojis['Language']} Language: {clan.chat_language}\n{Emojis['Invite']} Invitations type: {clan.type}\n{Emojis['Description']} Description: {escape_markdown(clan.description)}\n[Open in Clash of Clans]({clan.share_link})", interaction.guild.me.color, "For more information on clan members, send /members [tag]", interaction.guild.me.display_avatar.url)
    embed.set_thumbnail(url=clan.badge.url)
    return embed


async def clan_info(interaction: discord.Interaction, tag: str):
    try:
        embed = await clan_info_embed(interaction, tag)
    except coc.errors.NotFound:
        await interaction.response.send_message(f"Clan not found\nThere is no clan with the tag `{tag}`.", ephemeral=True)
        return
    await interaction.response.send_message(embed=embed)
    return
