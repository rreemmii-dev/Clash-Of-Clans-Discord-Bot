import discord

from bot.emojis import Emojis
from bot.functions import create_embed
from data.views import ComponentView


async def auto_roles_th(interaction: discord.Interaction, channel: discord.TextChannel):
    text = ""
    text += "Auto-Select to match your account(s) linked by `/link_coc_account`\n"
    for th_level, emoji in Emojis["Th_emojis"].items():
        role = discord.utils.get(interaction.guild.roles, name=f"Town Hall {th_level}")
        if role is None:
            role = await interaction.guild.create_role(name=f"Town Hall {th_level}")
        text += f"{emoji} to be {role.mention}\n"
    embed = create_embed("Select your town hall level to get the matching role", text, interaction.guild.me.color, "auto_roles_th", interaction.guild.me.display_avatar.url)
    if interaction.channel == channel:
        await interaction.response.send_message(embed=embed, view=ComponentView("auto_roles_th"))
    else:
        await channel.send(embed=embed, view=ComponentView("auto_roles_th"))
        await interaction.response.send_message("Done", ephemeral=True)
    return


async def auto_roles_bh(interaction: discord.Interaction, channel: discord.TextChannel):
    text = ""
    text += "Auto-Select to match your account(s) linked by `/link_coc_account`\n"
    for bh_level, emoji in Emojis["Bh_emojis"].items():
        role = discord.utils.get(interaction.guild.roles, name=f"Builder Hall {bh_level}")
        if role is None:
            role = await interaction.guild.create_role(name=f"Builder Hall {bh_level}")
        text += f"{emoji} to be {role.mention}\n"
    embed = create_embed("Select your builder hall level to get the matching role", text, interaction.guild.me.color, "auto_roles_bh", interaction.guild.me.display_avatar.url)
    if interaction.channel == channel:
        await interaction.response.send_message(embed=embed, view=ComponentView("auto_roles_bh"))
    else:
        await channel.send(embed=embed, view=ComponentView("auto_roles_bh"))
        await interaction.response.send_message("Done", ephemeral=True)
    return


async def auto_roles_leagues(interaction: discord.Interaction, channel: discord.TextChannel):
    text = ""
    text += "Auto-Select to match your account(s) linked by `/link_coc_account`\n"
    for league, emoji in Emojis["League_emojis"].items():
        role = discord.utils.get(interaction.guild.roles, name=league)
        if role is None:
            role = await interaction.guild.create_role(name=league)
        text += f"{emoji} to be {role.mention}\n"
    embed = create_embed("Select your league to get the matching role", text, interaction.guild.me.color, "auto_roles_leagues", interaction.guild.me.display_avatar.url)
    if interaction.channel == channel:
        await interaction.response.send_message(embed=embed, view=ComponentView("auto_roles_leagues"))
    else:
        await channel.send(embed=embed, view=ComponentView("auto_roles_leagues"))
        await interaction.response.send_message("Done", ephemeral=True)
    return
