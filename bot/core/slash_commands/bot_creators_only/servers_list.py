import os

import discord


async def servers_list(interaction: discord.Interaction):
    await interaction.response.defer()
    guilds = {}
    for guild in interaction.client.guilds:
        users = 0
        bots = 0
        for member in await guild.chunk(cache=False):
            if member.bot:
                bots += 1
            else:
                users += 1
        guilds[guild] = {"users": users, "bots": bots}
    ones = 0
    file = open("tmp.txt", "w")
    for guild in sorted(guilds.items(), key=lambda item: item[1]["users"], reverse=True):
        ones += 1
        text = f"\n{ones}) {guild[1]['users'] + guild[1]['bots']} members ({guild[1]['users']} users, {guild[1]['bots']} bots) ; creator: {guild[0].owner.name} ; server: {guild[0].name}"
        file.write(text)
    file.close()
    await interaction.followup.send(file=discord.File("tmp.txt"))
    os.remove("tmp.txt")
    return
