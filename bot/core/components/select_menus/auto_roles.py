import discord

from bot.emojis import Emojis
from data.useful import Useful


async def auto_roles_th(interaction: discord.Interaction):
    roles_list = []
    for th_level in range(1, Useful["max_th_lvl"] + 1):
        roles_list += [f"Town Hall {th_level}"]
    roles_to_remove = [role_name for role_name in roles_list if role_name.split(" ")[1] not in interaction.data["values"]]
    removed_roles = []
    for role_name in roles_to_remove:
        if role_name in [r.name for r in interaction.user.roles]:
            removed_roles += [role_name]
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role > interaction.guild.me.top_role:
                await interaction.response.send_message(f"The role `{role.name}` is higher than the bot highest role. Please put one of the bot roles higher than `{role.name}`", ephemeral=True)
                return
            else:
                await interaction.user.remove_roles(role)
    roles_to_add = [f"Town Hall {th_level}" for th_level in interaction.data["values"]]
    added_roles = []
    for role_name in roles_to_add:
        if role_name not in [r.name for r in interaction.user.roles]:
            added_roles += [role_name]
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role is None:
                role = await interaction.guild.create_role(name=role_name)
            if role > interaction.guild.me.top_role:
                await interaction.response.send_message(f"The role `{role.name}` is higher than the bot highest role. Please put one of the bot roles higher than `{role.name}`", ephemeral=True)
                return
            else:
                await interaction.user.add_roles(role)
    removed_roles.sort(key=lambda x: int(x.split(" ")[2]))
    removed_roles_str = ', '.join(removed_roles)
    added_roles.sort(key=lambda x: int(x.split(" ")[2]))
    added_roles_str = ', '.join(added_roles)
    await interaction.response.send_message(f"Roles removed: {removed_roles_str}\nRoles added: {added_roles_str}", ephemeral=True)
    return


async def auto_roles_bh(interaction: discord.Interaction):
    roles_list = []
    for bh_level in range(1, Useful["max_bh_lvl"] + 1):
        roles_list += [f"Builder Hall {bh_level}"]
    roles_to_remove = [role_name for role_name in roles_list if role_name.split(" ")[1] not in interaction.data["values"]]
    removed_roles = []
    for role_name in roles_to_remove:
        if role_name in [r.name for r in interaction.user.roles]:
            removed_roles += [role_name]
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role > interaction.guild.me.top_role:
                await interaction.response.send_message(f"The role `{role.name}` is higher than the bot highest role. Please put one of the bot roles higher than `{role.name}`", ephemeral=True)
                return
            else:
                await interaction.user.remove_roles(role)
    roles_to_add = [f"Builder Hall {bh_level}" for bh_level in interaction.data["values"]]
    added_roles = []
    for role_name in roles_to_add:
        if role_name not in [r.name for r in interaction.user.roles]:
            added_roles += [role_name]
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role is None:
                role = await interaction.guild.create_role(name=role_name)
            if role > interaction.guild.me.top_role:
                await interaction.response.send_message(f"The role `{role.name}` is higher than the bot highest role. Please put one of the bot roles higher than `{role.name}`", ephemeral=True)
                return
            else:
                await interaction.user.add_roles(role)
    removed_roles.sort(key=lambda x: int(x.split(" ")[2]))
    removed_roles_str = ', '.join(removed_roles)
    added_roles.sort(key=lambda x: int(x.split(" ")[2]))
    added_roles_str = ', '.join(added_roles)
    await interaction.response.send_message(f"Roles removed: {removed_roles_str}\nRoles added: {added_roles_str}", ephemeral=True)
    return


async def auto_roles_leagues(interaction: discord.Interaction):
    roles_list = []
    for league in Useful["league_trophies"].keys():
        roles_list += [league]
    roles_to_remove = [role_name for role_name in roles_list if role_name not in interaction.data["values"]]
    removed_roles = []
    for role_name in roles_to_remove:
        if role_name in [r.name for r in interaction.user.roles]:
            removed_roles += [role_name]
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role > interaction.guild.me.top_role:
                await interaction.response.send_message(f"The role `{role.name}` is higher than the bot highest role. Please put one of the bot roles higher than `{role.name}`", ephemeral=True)
                return
            else:
                await interaction.user.remove_roles(role)
    roles_to_add = [league for league in interaction.data["values"]]
    added_roles = []
    for role_name in roles_to_add:
        if role_name not in [r.name for r in interaction.user.roles]:
            added_roles += [role_name]
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role is None:
                role = await interaction.guild.create_role(name=role_name)
            if role > interaction.guild.me.top_role:
                await interaction.response.send_message(f"The role `{role.name}` is higher than the bot highest role. Please put one of the bot roles higher than `{role.name}`", ephemeral=True)
                return
            else:
                await interaction.user.add_roles(role)
    removed_roles.sort(key=lambda x: list(Emojis["League_emojis"].keys()).index(x))
    removed_roles_str = ', '.join(removed_roles)
    added_roles.sort(key=lambda x: list(Emojis["League_emojis"].keys()).index(x))
    added_roles_str = ', '.join(added_roles)
    await interaction.response.send_message(f"Roles removed: {removed_roles_str}\nRoles added: {added_roles_str}", ephemeral=True)
    return
