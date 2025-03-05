from typing import Union

import discord

from bot.emojis import Emojis
from data.useful import Useful


auto_roles_bh = discord.ui.Select(placeholder="Select your builder hall level", min_values=1, max_values=Useful["max_bh_lvl"])
auto_roles_bh.add_option(label="Auto-Select", value="auto")
for bh_level, emoji in Emojis["bh_emojis"].items():
    auto_roles_bh.add_option(label=f"Builder Hall {bh_level}", value=str(bh_level), emoji=emoji)

auto_roles_leagues = discord.ui.Select(placeholder="Select your league", min_values=1, max_values=len(Useful["league_trophies"].keys()))
auto_roles_leagues.add_option(label="Auto-Select", value="auto")
for league, emoji in Emojis["league_emojis"].items():
    auto_roles_leagues.add_option(label=league, value=league, emoji=emoji)

auto_roles_th = discord.ui.Select(placeholder="Select your town hall level", min_values=1, max_values=Useful["max_th_lvl"])
auto_roles_th.add_option(label="Auto-Select", value="auto")
for th_level, emoji in Emojis["th_emojis"].items():
    auto_roles_th.add_option(label=f"Town Hall {th_level}", value=str(th_level), emoji=emoji)

buildings_bh = discord.ui.Select(placeholder="Select your Builder Hall level", min_values=1, max_values=1)
for bh_level, emoji in Emojis["bh_emojis"].items():
    buildings_bh.add_option(label=f"BH {bh_level}", value=str(bh_level), emoji=emoji)

buildings_th = discord.ui.Select(placeholder="Select your Town Hall level", min_values=1, max_values=1)
for th_level, emoji in Emojis["th_emojis"].items():
    buildings_th.add_option(label=f"TH {th_level}", value=str(th_level), emoji=emoji)

player_info = discord.ui.Select(placeholder="Select the type of stats that you want to see", min_values=1, max_values=1)
player_info.add_option(label="Main", value="main", emoji=Emojis["th_emojis"][Useful["max_th_lvl"]])
player_info.add_option(label="Troops", value="troops", emoji=Emojis["troop"])
player_info.add_option(label="Success", value="success", emoji=Emojis["exp"])

button_follow = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Follow the support server news channel", emoji=Emojis["news"], custom_id="follow")
button_delete = discord.ui.Button(style=discord.ButtonStyle.danger, label="Delete this channel", emoji=Emojis["delete_grey"], custom_id="delete")


class ComponentView(discord.ui.View):
    def __init__(self, command: Union["auto_roles_bh", "auto_roles_leagues", "auto_roles_th", "buildings_bh", "buildings_th", "player_info", "joined_guild_message"]):
        super().__init__(timeout=None)
        if command == "auto_roles_bh":
            self.add_item(auto_roles_bh)
        elif command == "auto_roles_leagues":
            self.add_item(auto_roles_leagues)
        elif command == "auto_roles_th":
            self.add_item(auto_roles_th)
        elif command == "buildings_bh":
            self.add_item(buildings_bh)
        elif command == "buildings_th":
            self.add_item(buildings_th)
        elif command == "player_info":
            self.add_item(player_info)

        elif command == "joined_guild_message":
            self.add_item(button_follow)
            self.add_item(button_delete)
