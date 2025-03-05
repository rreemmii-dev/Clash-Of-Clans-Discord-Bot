import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown
from data.secure_folder import Linked_accounts


async def user_info(interaction: discord.Interaction, user: discord.User):
    accounts_linked = ""
    if user.id in Linked_accounts.keys():
        for k, v in Linked_accounts[user.id].items():
            if k == "Clash of Clans":
                for tag in v:
                    player = await Clash_of_clans.get_player(tag)
                    accounts_linked += f"{k}: {escape_markdown(player.name)} ({player.tag})\n"
            else:
                accounts_linked += f"{k}: {escape_markdown(', '.join(v))}\n"
    else:
        accounts_linked = "None\n"
    embed = create_embed(f"{escape_markdown(user.name)} ({escape_markdown(user.global_name)})", f"{Emojis['discord']} Discord account creation: **{user.created_at.date().isoformat()}**\n{Emojis['invite']} Server join: **{user.joined_at.date().isoformat()}**.\n\n{Emojis['member']} **Accounts linked:**\n{accounts_linked}", user.color, "", interaction.guild.me.display_avatar.url)
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
