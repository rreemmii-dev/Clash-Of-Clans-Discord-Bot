import json
import logging
import sqlite3
import traceback

import coc
import discord.errors
import nest_asyncio
from discord import app_commands

from bot.apis_clients.discord import Discord_token
from bot.core.slash_commands.army_link_analyze import army_link_analyze
from bot.core.slash_commands.auto_roles import auto_roles_bh, auto_roles_leagues, auto_roles_th
from bot.core.slash_commands.bot_creators_only.add_a_bot_id import add_a_bot_id
from bot.core.slash_commands.bot_creators_only.add_reaction_with_id import add_reaction_with_id
from bot.core.slash_commands.bot_creators_only.delete_messages import delete_message
from bot.core.slash_commands.bot_creators_only.download_emojis import download_emojis
from bot.core.slash_commands.bot_creators_only.find_user_by_id import find_user_by_id
from bot.core.slash_commands.bot_creators_only.reboot import reboot
from bot.core.slash_commands.bot_creators_only.refresh_dbl import refresh_dbl
from bot.core.slash_commands.bot_creators_only.servers_list import servers_list
from bot.core.slash_commands.bot_creators_only.stats import stats
from bot.core.slash_commands.bot_info import bot_info
from bot.core.slash_commands.buildings_bh import buildings_bh
from bot.core.slash_commands.buildings_th import buildings_th
from bot.core.slash_commands.clan_donations import clan_donations
from bot.core.slash_commands.clan_info import clan_info
from bot.core.slash_commands.clan_members import clan_members
from bot.core.slash_commands.clan_super_troops import clan_super_troops
from bot.core.slash_commands.clan_current_war import clan_current_war
from bot.core.slash_commands.help import help
from bot.core.slash_commands.link_coc_account import link_coc_account, unlink_coc_account
from bot.core.slash_commands.member_info import member_info
from bot.core.slash_commands.player_info import player_info
from bot.core.slash_commands.search_clan import search_clan
from bot.functions import *
from data.config import Config
from data.useful import Ids

votes_file = open(f"{Config['secure_folder_path']}votes.json", "r")
Votes = json.load(votes_file)

nest_asyncio.apply()

if __name__ == "__main__":
    from bot.apis_clients.discord import Clash_info

    connection_modifiable = sqlite3.connect(f"{Config['secure_folder_path']}secure.sqlite")
    cursor_modifiable = connection_modifiable.cursor()


    async def check_cmd_perms(interaction: discord.Interaction, command: str = None):
        if interaction.channel.type is discord.ChannelType.private:
            await interaction.response.send_message("Slash commands are not available in direct messages. Please add the bot to your server and then use slash commands there.")
            return -1
        if command is None:
            command = interaction.data["name"]
        if command == "_help":
            command = "help"

        from data.required_permissions import Required_permissions
        permissions_needed = Required_permissions[command]
        missing_bot_perms = []
        for perm in permissions_needed:
            if not getattr(interaction.app_permissions, perm):
                missing_bot_perms.append(perm)
        if missing_bot_perms:
            text = "the bot doesn't have the permission(s):"
            for perm in missing_bot_perms:
                text += f"\n{perm}"
            if len(missing_bot_perms) == 1:
                text += "\nPlease grant it to the bot and send again the command."
            else:
                text += "\nPlease grant them to the bot and send again the command."
            await interaction.response.send_message(f"Missing permissions: {text}")
            return -1
        return True


    def edit_commands_used(user_id: int, cmd: str):
        text = f"""INSERT INTO bot_usage(user_id) SELECT({user_id}) WHERE NOT EXISTS(SELECT 1 FROM bot_usage WHERE user_id={user_id})"""
        cursor_modifiable.execute(text)
        text = f"""UPDATE bot_usage SET {cmd} = (SELECT {cmd} FROM bot_usage WHERE user_id={user_id})+1 WHERE user_id={user_id}"""
        cursor_modifiable.execute(text)
        connection_modifiable.commit()


    command_tree = app_commands.CommandTree(Clash_info)

    async def on_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if type(error) is discord.app_commands.CommandInvokeError:
            if type(error.original) is discord.errors.NotFound:
                if interaction.app_permissions.send_messages:
                    await interaction.channel.send("The command has expired, please try again\n\n*This message will be deleted in 15 seconds*", delete_after=15)
        else:
            print(traceback.format_exc())
        return

    command_tree.on_error = on_error

    @command_tree.command(name="help", description="Show the help message to use @Clash INFO#3976")
    async def _help(interaction: discord.Interaction):
        if await check_cmd_perms(interaction) == -1:
            return
        await help(interaction)
        edit_commands_used(interaction.user.id, "help")
        return

    @command_tree.command(name="_help", description="Show the help message to use @Clash INFO#3976")
    async def __help(interaction: discord.Interaction):
        if await check_cmd_perms(interaction) == -1:
            return
        await help(interaction)
        edit_commands_used(interaction.user.id, "help")
        return


    # Clash Of Clans
    @command_tree.command(name="army_link_analyze", description="Show the troops and spells from an in-game army link")
    @app_commands.describe(army_link="Army link, gettable from Clash Of Clans > Army > Quick Train > Share > Share as link")
    async def _army_link_analyze(interaction: discord.Interaction, army_link: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await army_link_analyze(interaction, army_link)
        edit_commands_used(interaction.user.id, "army_link_analyze")
        return

    @command_tree.command(name="auto_roles_bh", description="[Administrators only] Create an auto-roles system to give the BH level roles")
    @app_commands.guild_only()
    @app_commands.describe(channel="Channel where it will be the auto-roles system")
    @app_commands.default_permissions(administrator=True)
    async def _auto_roles_bh(interaction: discord.Interaction, channel: discord.TextChannel = None):
        if await check_cmd_perms(interaction) == -1:
            return
        if channel is None:
            channel = interaction.channel
        await auto_roles_bh(interaction, channel)
        edit_commands_used(interaction.user.id, "auto_roles_bh")
        return

    @command_tree.command(name="auto_roles_leagues", description="[Administrators only] Create an auto-roles system to give the league role")
    @app_commands.guild_only()
    @app_commands.describe(channel="Channel where it will be the auto-roles system")
    @app_commands.default_permissions(administrator=True)
    async def _auto_roles_leagues(interaction: discord.Interaction, channel: discord.TextChannel = None):
        if await check_cmd_perms(interaction) == -1:
            return
        if channel is None:
            channel = interaction.channel
        await auto_roles_leagues(interaction, channel)
        edit_commands_used(interaction.user.id, "auto_roles_leagues")
        return

    @command_tree.command(name="auto_roles_th", description="[Administrators only] Create an auto-roles system to give the TH level roles")
    @app_commands.guild_only()
    @app_commands.describe(channel="Channel where it will be the auto-roles system")
    @app_commands.default_permissions(administrator=True)
    async def _auto_roles_th(interaction: discord.Interaction, channel: discord.TextChannel = None):
        if await check_cmd_perms(interaction) == -1:
            return
        if channel is None:
            channel = interaction.channel
        await auto_roles_th(interaction, channel)
        edit_commands_used(interaction.user.id, "auto_roles_th")
        return

    @command_tree.command(name="buildings_bh", description="Show the maximum level for each buildings at the given Builder Hall level")
    @app_commands.describe(builder_hall_level="Builder Hall level")
    async def _buildings_bh(interaction: discord.Interaction, builder_hall_level: int = 0):
        if await check_cmd_perms(interaction) == -1:
            return
        await buildings_bh(interaction, builder_hall_level)
        edit_commands_used(interaction.user.id, "buildings_bh")
        return

    @command_tree.command(name="buildings_th", description="Show the maximum level for each buildings at the given Town Hall level")
    @app_commands.describe(town_hall_level="Town Hall level")
    async def _buildings_th(interaction: discord.Interaction, town_hall_level: int = 0):
        if await check_cmd_perms(interaction) == -1:
            return
        await buildings_th(interaction, town_hall_level)
        edit_commands_used(interaction.user.id, "buildings_th")
        return

    @command_tree.command(name="clan_donations", description="Show the clan members, sorted by donations stats")
    @app_commands.describe(clan_tag="Clash Of Clans clan tag, format: #A1B2C3D4")
    async def _clan_donations(interaction: discord.Interaction, clan_tag: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await clan_donations(interaction, clan_tag)
        edit_commands_used(interaction.user.id, "clan_donations")
        return

    @command_tree.command(name="clan_info", description="Show data about the clan")
    @app_commands.describe(clan_tag="Clash Of Clans clan tag, format: #A1B2C3D4")
    async def _clan_info(interaction: discord.Interaction, clan_tag: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await clan_info(interaction, clan_tag)
        edit_commands_used(interaction.user.id, "clan_info")
        return

    @command_tree.command(name="clan_members", description="Show the clan members")
    @app_commands.describe(clan_tag="Clash Of Clans clan tag, format: #A1B2C3D4")
    async def _clan_members(interaction: discord.Interaction, clan_tag: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await clan_members(interaction, clan_tag)
        edit_commands_used(interaction.user.id, "clan_members")
        return

    @command_tree.command(name="clan_current_war", description="Show data about the clan war")
    @app_commands.describe(clan_tag="Clash Of Clans clan tag, format: #A1B2C3D4")
    async def _clan_current_war(interaction: discord.Interaction, clan_tag: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await clan_current_war(interaction, clan_tag)
        edit_commands_used(interaction.user.id, "clan_current_war")
        return

    @command_tree.command(name="player_info", description="Show data about the player")
    @app_commands.describe(player_tag="Clash Of Clans player tag, format: #A1B2C3D4")
    @app_commands.describe(information="Information wanted")
    @app_commands.choices(information=[
        app_commands.Choice(name="main", value="main"),
        app_commands.Choice(name="troops", value="troops"),
        app_commands.Choice(name="success", value="success")
    ])
    async def _player_info(interaction: discord.Interaction, player_tag: str, information: app_commands.Choice[str]):
        if await check_cmd_perms(interaction) == -1:
            return
        await player_info(interaction, player_tag, information.value)
        edit_commands_used(interaction.user.id, "player_info")
        return

    @command_tree.command(name="search_clan", description="Search clans by name")
    @app_commands.describe(name="Clan name")
    async def _search_clan(interaction: discord.Interaction, name: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await search_clan(interaction, name)
        edit_commands_used(interaction.user.id, "search_clan")
        return

    @command_tree.command(name="clan_super_troops", description="Show which super troop has been activated, and by which player of the clan")
    @app_commands.describe(clan_tag="Clash Of Clans clan tag, format: #A1B2C3D4")
    async def _clan_super_troops(interaction: discord.Interaction, clan_tag: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await clan_super_troops(interaction, clan_tag)
        edit_commands_used(interaction.user.id, "clan_super_troops")
        return

    @command_tree.command(name="link_coc_account", description="Link your Clash Of Clans account to your Discord account")
    @app_commands.describe(player_tag="Clash Of Clans player tag, format: #A1B2C3D4")
    @app_commands.describe(api_token="Your API token, findable in Clash Of Clans > Settings > More Settings > API Token > Show")
    async def _link_coc_account(interaction: discord.Interaction, player_tag: str, api_token: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await link_coc_account(interaction, player_tag, api_token)
        edit_commands_used(interaction.user.id, "link_coc_account")
        return

    @command_tree.command(name="unlink_coc_account", description="Unlink your Clash Of Clans account from your Discord account")
    @app_commands.describe(player_tag="Clash Of Clans player tag, format: #A1B2C3D4")
    async def _unlink_coc_account(interaction: discord.Interaction, player_tag: str):
        if await check_cmd_perms(interaction) == -1:
            return
        await unlink_coc_account(interaction, player_tag)
        edit_commands_used(interaction.user.id, "unlink_coc_account")
        return

    @command_tree.command(name="member_info", description="Show permissions, when the member joined Discord / the server and their avatar")
    @app_commands.describe(member="The member")
    async def _member_info(interaction: discord.Interaction, member: discord.Member):
        if await check_cmd_perms(interaction) == -1:
            return
        await member_info(interaction, member)
        edit_commands_used(interaction.user.id, "member_info")
        return

    @command_tree.command(name="bot_info", description="Show some information about the bot")
    async def _bot_info(interaction: discord.Interaction):
        if await check_cmd_perms(interaction) == -1:
            return
        await bot_info(interaction)
        edit_commands_used(interaction.user.id, "bot_info")
        return

    # CREATORS
    @command_tree.command(name="__add_a_bot_id", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Add the bot with the given id")
    async def ___add_a_bot_id(interaction: discord.Interaction, bot_id: str):
        await add_a_bot_id(interaction, int(bot_id))
        return

    @command_tree.command(name="__add_reaction_with_id", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Add a reaction everywhere with the channel/message/emoji ids")
    async def ___add_reaction_with_id(interaction: discord.Interaction, channel_id: str, message_id: str, emoji_id: str):
        await add_reaction_with_id(interaction, int(channel_id), int(message_id), int(emoji_id))
        return

    @command_tree.command(name="__delete_messages", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Delete messages quickly")
    async def ___delete_messages(interaction: discord.Interaction, channel_id: str, number: int):
        await delete_message(interaction, int(channel_id), number)
        return

    @command_tree.command(name="__download_emojis", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Send a .zip message with the emojis of emojis channels")
    @app_commands.choices(recreate_emojis_zip=[
        app_commands.Choice(name="True", value=1),
        app_commands.Choice(name="False", value=0)
    ])
    async def ___download_emojis(interaction: discord.Interaction, recreate_emojis_zip: app_commands.Choice[int]):
        await download_emojis(interaction, bool(recreate_emojis_zip.value))
        return

    @command_tree.command(name="__find_user_by_id", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Find the user with the given id")
    async def ___find_user_by_id(interaction: discord.Interaction, user_id: str):
        await find_user_by_id(interaction, int(user_id))
        return

    @command_tree.command(name="__reboot", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Reboot the Raspberry Pi")
    async def ___reboot(interaction: discord.Interaction):
        await reboot(interaction)
        return

    @command_tree.command(name="__refresh_dbl", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Refresh the top.gg servers counter")
    async def ___refresh_dbl(interaction: discord.Interaction):
        await refresh_dbl(interaction)
        return

    @command_tree.command(name="__servers_list", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Show all the servers with the bot")
    async def ___servers_list(interaction: discord.Interaction):
        await servers_list(interaction)
        return

    @command_tree.command(name="__stats", guild=discord.Object(id=Ids["Bot_creators_only_server"]), description="Show monthly usages")
    async def ___stats(interaction: discord.Interaction):
        await stats(interaction)
        return


    @Clash_info.event
    async def on_interaction(interaction: discord.Interaction):
        if interaction.type is discord.InteractionType.component:
            try:
                if interaction.message.embeds[0].footer.text == "joined_guild_message":
                    from bot.core.components.buttons.joined_guild_message import joined_guild_message
                    await joined_guild_message(interaction)
                    return
                footer_text = interaction.message.embeds[0].footer.text
                command_name = footer_text.split("|")[0]
                if command_name == "auto_roles_bh" or command_name == "auto_roles bh":
                    if await check_cmd_perms(interaction, command="auto_roles_bh") == -1:
                        return
                    from bot.core.components.select_menus.auto_roles import auto_roles_bh
                    await auto_roles_bh(interaction)
                    return
                elif command_name == "auto_roles_leagues" or command_name == "auto_roles_league" or command_name == "auto_roles league":
                    if await check_cmd_perms(interaction, command="auto_roles_leagues") == -1:
                        return
                    from bot.core.components.select_menus.auto_roles import auto_roles_leagues
                    await auto_roles_leagues(interaction)
                    return
                elif command_name == "auto_roles_th" or command_name == "auto_roles th":
                    if await check_cmd_perms(interaction, command="auto_roles_th") == -1:
                        return
                    from bot.core.components.select_menus.auto_roles import auto_roles_th
                    await auto_roles_th(interaction)
                    return
                if interaction.user.id == int(footer_text.split("|")[-1]):
                    if command_name == "buildings_bh":
                        if await check_cmd_perms(interaction, command="buildings_bh") == -1:
                            return
                        from bot.core.components.select_menus.change_bh_lvl import change_bh_lvl
                        await change_bh_lvl(interaction)
                        return
                    elif command_name == "buildings_th":
                        if await check_cmd_perms(interaction, command="buildings_th") == -1:
                            return
                        from bot.core.components.select_menus.change_th_lvl import change_th_lvl
                        await change_th_lvl(interaction)
                        return
                    elif command_name == "search_clan":
                        if await check_cmd_perms(interaction, command="search_clan") == -1:
                            return
                        from bot.core.components.select_menus.change_search_clan import change_search_clan
                        await change_search_clan(interaction)
                        return
                    elif command_name == "player_info":
                        if await check_cmd_perms(interaction, command="player_info") == -1:
                            return
                        from bot.core.components.select_menus.change_player_info_page import change_player_stats_page
                        await change_player_stats_page(interaction)
                        return
                else:
                    await interaction.response.send_message("You can only use select menu of slash commands sent by you", ephemeral=True)

            except discord.errors.NotFound:
                await interaction.channel.send("The command has expired, please try again\n\n*This message will be deleted in 15 seconds*", delete_after=15)
        return


    async def sync_commands():
        await command_tree.sync()
        await command_tree.sync(guild=discord.Object(id=Ids["Test_server"]))
        await command_tree.sync(guild=discord.Object(id=Ids["Bot_creators_only_server"]))

    Clash_info.sync_commands = sync_commands
    # Clash_info.run(Discord_token, log_handler=logging.StreamHandler(), log_level=logging.INFO)
    while True:
        try:
            Clash_info.run(Discord_token, log_handler=logging.StreamHandler(), log_level=logging.INFO)
        except Exception as e:
            print(f"\n\nError : {e}\n\n")
