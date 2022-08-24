import coc
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown, cardinal_to_ordinal_number, trophies_to_league


async def clan_members(interaction: discord.Interaction, tag: str):
    try:
        clan = await Clash_of_clans.get_clan(tag)
    except coc.errors.NotFound:
        await interaction.response.send_message(f"Clan not found\nThere is no clan with the tag `{tag}`.", ephemeral=True)
        return
    text = ""
    x = 0
    rank = 0
    embeds = []
    async for member in clan.get_detailed_members():
        rank += 1
        text += f"{cardinal_to_ordinal_number(rank)} | {trophies_to_league(member.trophies)} {member.trophies} | {Emojis['Th_emojis'][member.town_hall]} | {Emojis['Exp']} {member.exp_level} | {escape_markdown(member.name)}: {member.tag}\n"
        x += 1
        if x == 25:
            embed = create_embed(f"Clan members {escape_markdown(clan.name)} ({clan.tag})", f"Members list: \n{text}", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
            embeds += [embed]
            text = ""
            x = 0
    if x != 0:
        embed = create_embed(f"Clan members {escape_markdown(clan.name)} ({clan.tag})", f"Members list: \n{text}", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
        embeds += [embed]
    if (lambda l: sum([len(item) for item in l]))(embeds) <= 6000:
        await interaction.response.send_message(embeds=embeds)
    else:
        await interaction.response.send_message(embed=embeds[0])
        if len(embeds) > 1:
            await interaction.channel.send(embed=embeds[1])
    return
