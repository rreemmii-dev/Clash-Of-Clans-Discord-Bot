import discord

from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown
from data.secure_folder import Linked_accounts


async def member_info(interaction: discord.Interaction, member: discord.Member):
    accounts_linked = ""
    if member.id in Linked_accounts.keys():
        for k, v in Linked_accounts[member.id].items():
            accounts_linked += f"{k}: {escape_markdown(', '.join(v))}"
    else:
        accounts_linked = "None"
    member_permissions = ""
    if member.guild_permissions.administrator:
        member_permissions += "Administrator\n"
    if member.guild_permissions.manage_guild:
        member_permissions += "Manage server\n"
    if member.guild_permissions.manage_roles:
        member_permissions += "Manage roles\n"
    if member.guild_permissions.manage_permissions:
        member_permissions += "Manage permissions\n"
    if member.guild_permissions.manage_events:
        member_permissions += "Manage events\n"
    if member.guild_permissions.manage_emojis_and_stickers:
        member_permissions += "Manage emojis and stickers\n"
    if member.guild_permissions.manage_channels:
        member_permissions += "Manage channels\n"
    if member.guild_permissions.manage_threads:
        member_permissions += "Manage threads\n"
    if member.guild_permissions.manage_messages:
        member_permissions += "Manage messages\n"
    if member.guild_permissions.manage_webhooks:
        member_permissions += "Manage webhooks\n"
    if member.guild_permissions.ban_members:
        member_permissions += "Ban members\n"
    if member.guild_permissions.kick_members:
        member_permissions += "Kick members\n"
    if member.guild_permissions.moderate_members:
        member_permissions += "Moderate members\n"
    if member.guild_permissions.manage_nicknames:
        member_permissions += "Manage nicknames\n"
    if member.guild_permissions.mention_everyone:
        member_permissions += "Mention everyone\n"
    if member.guild_permissions.view_audit_log:
        member_permissions += "View logs\n"
    if member_permissions == "":
        member_permissions = "Any"
    embed = create_embed(escape_markdown(member.name), f"{Emojis['Invite']} Server join: **{member.joined_at.date().isoformat()}**.\n{Emojis['Discord']} Discord account creation: **{member.created_at.date().isoformat()}**\n\n{Emojis['Member']} **Accounts linked:**\n{accounts_linked}\n\n{Emojis['Settings']} **Member permissions:**\n{member_permissions}", member.color, "", interaction.guild.me.display_avatar.url)
    embed.set_thumbnail(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
