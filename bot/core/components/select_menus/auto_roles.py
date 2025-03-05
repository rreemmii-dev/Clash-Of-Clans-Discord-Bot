import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from data.secure_folder import Linked_accounts
from data.useful import Useful


async def auto_roles_th(interaction: discord.Interaction):
    roles_list = []
    for th_level in range(1, Useful["max_th_lvl"] + 1):
        roles_list += [f"Town Hall {th_level}"]
    chosen = list(interaction.data["values"])
    if "auto" in chosen:
        chosen.remove("auto")
        user = interaction.user
        if user.id in Linked_accounts.keys():
            for k, v in Linked_accounts[user.id].items():
                if k == "Clash of Clans":
                    for tag in v:
                        player = await Clash_of_clans.get_player(tag)
                        th = str(player.town_hall)
                        if th not in chosen:
                            chosen.append(th)
    roles_to_remove = [role_name for role_name in roles_list if role_name.split(" ")[2] not in chosen]
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
    roles_to_add = [f"Town Hall {th_level}" for th_level in chosen]
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
    chosen = list(interaction.data["values"])
    if "auto" in chosen:
        chosen.remove("auto")
        user = interaction.user
        if user.id in Linked_accounts.keys():
            for k, v in Linked_accounts[user.id].items():
                if k == "Clash of Clans":
                    for tag in v:
                        player = await Clash_of_clans.get_player(tag)
                        bh = str(player.builder_hall)
                        if bh not in chosen and player.builder_hall >= 1:
                            chosen.append(bh)
    roles_to_remove = [role_name for role_name in roles_list if role_name.split(" ")[2] not in chosen]
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
    roles_to_add = [f"Builder Hall {bh_level}" for bh_level in chosen]
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
    chosen = list(interaction.data["values"])
    if "auto" in chosen:
        chosen.remove("auto")
        user = interaction.user
        if user.id in Linked_accounts.keys():
            for k, v in Linked_accounts[user.id].items():
                if k == "Clash of Clans":
                    for tag in v:
                        player = await Clash_of_clans.get_player(tag)
                        league = f"{player.league.name} League"
                        if league not in chosen:
                            chosen.append(league)
    roles_to_remove = [role_name for role_name in roles_list if role_name not in chosen]
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
    roles_to_add = [league for league in chosen]
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
    removed_roles.sort(key=lambda x: list(Emojis["league_emojis"].keys()).index(x))
    removed_roles_str = ', '.join(removed_roles)
    added_roles.sort(key=lambda x: list(Emojis["league_emojis"].keys()).index(x))
    added_roles_str = ', '.join(added_roles)
    await interaction.response.send_message(f"Roles removed: {removed_roles_str}\nRoles added: {added_roles_str}", ephemeral=True)
    return
