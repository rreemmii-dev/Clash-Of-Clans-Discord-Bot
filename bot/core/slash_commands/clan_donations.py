import coc
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.functions import cardinal_to_ordinal_number, create_embed, escape_markdown


async def clan_donations(interaction: discord.Interaction, tag: str):
    try:
        clan = await Clash_of_clans.get_clan(tag)
    except coc.errors.NotFound:
        await interaction.response.send_message(f"Clan not found\nThere is no clan with the tag `{tag}`.", ephemeral=True)
        return
    donations = {}
    for member in clan.members:
        if member.received == 0:
            if member.donations == 0:
                ratio = 1
            else:
                ratio = member.donations
        else:
            ratio = member.donations/member.received
        ratio = round(ratio*100)
        diff = member.donations - member.received
        donations[member.tag] = {"difference": diff, "ratio": ratio, "donations": member.donations, "received": member.received, "member": member}
    donations_list = sorted(donations, key=lambda m: donations[m]["difference"], reverse=True)
    description = ""
    x = 0
    rank = 0
    embeds = []
    for member_tag in donations_list:
        member_dict = donations[member_tag]
        member = member_dict["member"]
        rank += 1
        description += f"{cardinal_to_ordinal_number(rank)} | {member_dict['difference']:+} (= {member_dict['donations']} - {member_dict['received']}) | {member_dict['ratio']}% | {escape_markdown(member.name)} ({member.tag})\n"
        x += 1
        if x == 25:
            embed = create_embed(f"Clan donations: {escape_markdown(clan.name)} ({clan.tag})", f"*Rank | Difference (Donations - Received) | Ratio (%)*\n{description}", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
            embeds += [embed]
            description = ""
            x = 0
    if x != 0:
        embed = create_embed(f"Clan donations: {escape_markdown(clan.name)} ({clan.tag})", f"*Rank | Difference (Donations - Received) | Ratio (%)* \n{description}", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
        embeds += [embed]
    if (lambda l: sum([len(item) for item in l]))(embeds) <= 6000:
        await interaction.response.send_message(embeds=embeds)
    else:
        await interaction.response.send_message(embed=embeds[0])
        if len(embeds) > 1:
            await interaction.channel.send(embed=embeds[1])
    return
