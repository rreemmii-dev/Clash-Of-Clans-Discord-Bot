import json

import coc.utils
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.functions import create_embed
from data.config import Config
from data.secure_folder import Linked_accounts


async def link_coc_account(interaction: discord.Interaction, player_tag: str, api_token: str):
    api_token = api_token.upper()
    player_tag = coc.utils.correct_tag(player_tag)
    is_correct_token = await Clash_of_clans.verify_player_token(player_tag, api_token)
    if is_correct_token:
        if interaction.user.id not in Linked_accounts.keys():
            Linked_accounts[interaction.user.id] = {"Clash Of Clans": []}
        if player_tag not in Linked_accounts[interaction.user.id]["Clash Of Clans"]:
            Linked_accounts[interaction.user.id]["Clash Of Clans"] = Linked_accounts[interaction.user.id]["Clash Of Clans"] + [player_tag]
            json_text = json.dumps(Linked_accounts, sort_keys=True, indent=4)
            linked_account_file = open(f"{Config['secure_folder_path']}linked_accounts.json", "w")
            linked_account_file.write(json_text)
            linked_account_file.close()
            embed = create_embed("Accounts linked", f"Your Discord account is now linked with the Clash Of Clans account `{player_tag}`", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f"Your Discord account is already linked with the Clash Of Clans account `{player_tag}`")
    else:
        await interaction.response.send_message(f"The token {api_token} does not match with the tag {player_tag}", ephemeral=True)
    return


async def unlink_coc_account(interaction: discord.Interaction, player_tag: str):
    player_tag = coc.utils.correct_tag(player_tag)
    if interaction.user.id in Linked_accounts.keys() and player_tag in Linked_accounts[interaction.user.id]["Clash Of Clans"]:
        Linked_accounts[interaction.user.id]["Clash Of Clans"].pop(Linked_accounts[interaction.user.id]["Clash Of Clans"].index(player_tag))
        if not Linked_accounts[interaction.user.id]["Clash Of Clans"]:
            Linked_accounts.pop(interaction.user.id)
        json_text = json.dumps(Linked_accounts, sort_keys=True, indent=4)
        linked_account_file = open(f"{Config['secure_folder_path']}linked_accounts.json", "w")
        linked_account_file.write(json_text)
        linked_account_file.close()
        embed = create_embed("Accounts unlinked", f"Your Discord account is no longer linked with the Clash Of Clans account `{player_tag}`", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = create_embed("Account not linked", f"Your Discord account is not linked with the Clash Of Clans account `{player_tag}`", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    return
