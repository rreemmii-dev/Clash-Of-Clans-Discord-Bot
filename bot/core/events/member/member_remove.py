import datetime

import discord

from bot.functions import create_embed, escape_markdown
from data.useful import Ids


async def member_remove(self: discord.AutoShardedClient, member: discord.Member):
    if member.guild.id == Ids["Support_server"]:
        users = 0
        for m in member.guild.members:
            if not m.bot:
                users += 1
        for channel in member.guild.channels:
            if channel.name.startswith("👤 "):
                await channel.edit(name=f"👤 Users: {users: ,}")
                break
        else:
            overwrite = {member.guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)}
            await member.guild.create_voice_channel(f"👤 Users: {users: ,}", overwrites=overwrite)

        welcome = member.guild.get_channel(Ids["Welcome_channel"])
        days_spent_in_the_server = (datetime.datetime.now().date() - member.joined_at.date()).days
        if days_spent_in_the_server > 1:
            embed = create_embed(f"Unfortunately, {escape_markdown(member.name)} left us", f"{escape_markdown(member.name)}#{member.discriminator} (`{member.id}`) left us. He/She joined the server the {member.joined_at.date().isoformat()} ({days_spent_in_the_server} days ago)", member.color, "", member.guild.me.display_avatar.url)
            embed.set_thumbnail(url=member.display_avatar.url)
            await welcome.send(embed=embed)
        else:
            async for message in welcome.history(limit=None):
                old_embed = message.embeds[0]
                if int(old_embed.description.split("`")[-2]) == member.id:
                    if message.author == message.guild.me:
                        new_embed = old_embed.copy()
                        new_embed.description = old_embed.description + f"\n*Unfortunately, {escape_markdown(member.name)} left us after less than a day in the server*"
                        new_embed.set_image(url="attachment://Welcome.png")
                        await message.edit(embed=new_embed)
                        break
    return
