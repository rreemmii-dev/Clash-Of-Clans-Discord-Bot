# Clash-Of-Clans-Discord-Bot


[![Discord](https://img.shields.io/discord/719537805604290650?color=%230000ff&label=Discord&logo=https%3A%2F%2Fdiscord.com%2Fassets%2F2c21aeda16de354ba5334551a883b481.png&logoColor=%2300000000)](https://discord.gg/KQmstPw)
[![Python version](https://img.shields.io/badge/Python-%E2%89%A5%203.8-blue)](https://www.python.org/downloads/)
[![GitHub Repo stars](https://img.shields.io/github/stars/rreemmii-dev/Clash-Of-Clans-Discord-Bot?label=Stars)](https://github.com/rreemmii-dev/Clash-Of-Clans-Discord-Bot/stargazers)
[![GitHub contributors](https://img.shields.io/github/contributors/rreemmii-dev/Clash-Of-Clans-Discord-Bot?label=Contributors)](https://github.com/rreemmii-dev/Clash-Of-Clans-Discord-Bot/graphs/contributors)


**This project is a Discord Bot about the game Clash of Clans. It uses especially the [discord.py](https://github.com/Rapptz/discord.py) and [coc.py](https://github.com/mathsman5133/coc.py) libraries.**

If you want to test the bot, you can [add it to your server](https://rreemmii-dev.github.io/clash-info/invite). You can also join the [support server](https://discord.gg/KQmstPw) to test the bot or to ask for help.


## Table of contents

- [Installation + Setup](#installation--setup)
- [Usage](#usage)
- [Features](#features)
- [Support](#support)
- [License](#license)


## Installation + Setup

```shell
# Clone the main branch:
git clone https://github.com/rreemmii-dev/Clash-Of-Clans-Discord-Bot.git --single-branch

# Download the libraries:
pip install -r Clash-Of-Clans-Discord-Bot\requirements.txt
```

You must follow these steps to create and set up your bot:
- Create a bot following [these steps](https://discordpy.readthedocs.io/en/latest/discord.html). For your invite link, add the `bot` and `applications.commands` scopes, and the required permissions given [here](data/data_source/useful.json) (or the `administrator` permission).
- You will need the [member privileged intent](https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents) to run the bot. If your bot is in more than 100 servers, you have to make a request for additional intents, which is usually satisfied within a week.
- Unzip [Emojis.zip](Emojis.zip). Then, create a server for each folder (you will have about 8 servers for emojis), and add emojis from each folder to the matching server. Finally, add your bot in each of these servers.

Once it's done, you have to edit the [bot/config.json](bot/config.json) file and fill in the [data/data_source/ids.json](data/data_source/ids.json). You have also to rename the [secure_folder_template](secure_folder_template) to "Secure Folder" and add your credentials in your [Secure Folder/login.json](secure_folder_template/login.json) file.

<details>
<summary>

#### Help to edit the [bot/config.json](bot/config.json) file.

</summary>

In this file, you can choose whether to activate or not some parts of the code (e.g. parts using Discord Intents). You have also some initialization of variables to do.

| Field                    | Description                                                                                                                                                       | Requirements                                                                                                                                                                                                                                            |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `main_bot`               | Setting it to `false` will run a beta bot for tests, while setting it to `true` will run your main bot.                                                           | You need two bots to use them as beta and main bots. However, you can only use a main bot, and let `main_bot` at `true`.                                                                                                                                |
| `top_gg`                 | You can interact with the [top.gg](https://top.gg) API to refresh the bot guilds count.                                                                           | You need to register your bot on [top.gg](https://top.gg).                                                                                                                                                                                              |
| `top_gg_webhooks`        | If it's enabled, you will receive a webhook when someone vote for your bot.                                                                                       | You need to register your bot on [top.gg](https://top.gg).<br/>Then, go to https://top.gg/bot/[bot_id]/webhooks and put http://[your_public_ip_address]:8080/topgg_webhook for "Webhook URL". Do not forget to do a port forwarding for your 8080 port. |

</details>

<details>
<summary>

#### Help to fill in the [data/data_source/ids.json](data/data_source/ids.json) file.

</summary>

In this file, you will have to put the ID of each user, role, server or channel.

| Field                               | Description                                                                                                                                                                                                     |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Users                               |                                                                                                                                                                                                                 |
| `Creators`                          | List of bot creators ids. It is only used to give an access to some text commands like `dltmsg`. Slash commands for creators are set with the `Bot_creators_only_server`.                                       |
| `Bot`                               | Main bot id.                                                                                                                                                                                                    |
| `Bot_beta`                          | Beta bot id.                                                                                                                                                                                                    |
| Servers                             |                                                                                                                                                                                                                 |
| `Support_server`                    | Support server id. You have some functions only for the support server (e.g. Auto-moderation).                                                                                                                  |
| `Test_server`                       | A test server (slash commands synchronization is faster there). You can put your support server id or another.                                                                                                  |
| `Bot_creators_only_server`          | The server where all the slash commands for bot creators are. Everybody in this server will be able to use the slash commands for creators, so make sure only bot creators are in this server.                  |
| `Emojis_coc_players_related_server` | The server with the emojis that are related to players (Town Halls, Builder Halls, leagues and heroes).                                                                                                         |
| `Emojis_coc_troops_server`          | The server with emojis of troops, spells, siege machines and pets.                                                                                                                                              |
| `Emojis_coc_clans_related_server`   | The server with emojis that are related to clans (war leagues).                                                                                                                                                 |
| `Emojis_coc_remains_server`         | The server with all remaining emojis about Clash of Clans.                                                                                                                                                      |
| `Emojis_discord_main_server`        | The server with emojis of Discord User Interface.                                                                                                                                                               |
| `Emojis_general_remains_server`     | The server with all remaining emojis.                                                                                                                                                                           |
| Roles                               |                                                                                                                                                                                                                 |
| `Member_role`                       | Member role id. This role will be given to every member of your server (excepted bots). This role must belong to your support server. You can leave this field empty to disable this feature.                   |
| `Staff_role`                        | Staff role id. The auto moderation doesn't apply for members with this role. This role must belong to your support server.                                                                                      |
| Channels                            |                                                                                                                                                                                                                 |
| `Weekly_stats_channel`              | The channel where the bot sends a weekly message with the servers number evolution.                                                                                                                             |
| `Monthly_stats_channel`             | The channel were the bot sends a monthly message about its usage stats.                                                                                                                                         |
| `News_channel`                      | The news channel where announcements about the bot are sent. This channel must belong to your support server.                                                                                                   |
| `Rules_channel`                     | The rules channel of the support server. This channel must belong to your support server.                                                                                                                       |
| `Status_channel`                    | The channel where the bot sends a message when it's connected, and when the cache is loaded.                                                                                                                    |
| `Guilds_bot_log_channel`            | The channel were the bot sends a message when it joins/leaves a server with more than 100 users (bot are not considered as users). For privacy reasons, please put this channel in the server for bot creators. |
| `Dm_bot_log_channel`                | The channel with the logs of messages sent to the bot by DMs. For privacy reasons, please put this channel in the server for bot creators.                                                                      |
| `Votes_channel`                     | The channel where messages are sent when someone vote for the bot on [top.gg](https://top.gg), with a vote counter per user. For privacy reasons, please put this channel in the server for bot creators.       |
| `Welcome_channel`                   | The channel where the bot sends a welcome message when a new member arrives. This channel must belong to your support server.                                                                                   |
| `Secure_folder_backup_channel`      | The channel where the backups of the Secure Folder are sent every week. For privacy reasons, please put this channel in the server for bot creators.                                                            |
| `Events_github_channel`             | The channel where the events from GitHub webhooks will be posted.                                                                                                                                               |


</details>

<details>
<summary>

#### Help about the Secure Folder

</summary>

First, you have to rename the [secure_folder_template](secure_folder_template) to "Secure Folder".

Then, you have to fill in your [Secure Folder/login.json](secure_folder_template/login.json) file with your credentials. You can see in the following table when each field is required, and how to get the credential.

| Field                                        | When is it required ?                                         | How to get it ?                                                     |
|----------------------------------------------|---------------------------------------------------------------|---------------------------------------------------------------------|
| `discord > main`                             | Always Required                                               | Help here: https://discordpy.readthedocs.io/en/latest/discord.html  |
| `discord > beta`                             | Used if `main_bot` is set to `false` in bot/config.json       | Help here: https://discordpy.readthedocs.io/en/latest/discord.html  |
| `clash_of_clans > main > [email / password]` | Always Required                                               | You have to create an account in https://developer.clashofclans.com |
| `clash_of_clans > beta > [email / password]` | Used if `main_bot` is set to `false` in bot/config.json       | You have to create an account in https://developer.clashofclans.com |
| `top_gg > token`                             | Used if `top_gg` is set to `true` in bot/config.json          | Got from https://top.gg/bot/[bot_id]/webhooks                       |
| `top_gg > authorization`                     | Used if `top_gg_webhooks` is set to `true` in bot/config.json | You have to set it in https://top.gg/bot/[bot_id]/webhooks          |

</details>

That's it! You can now run the script

```shell
# Run the script:
python Clash-Of-Clans-Discord-Bot\main.py
```


## Usage

<details>
<summary>

#### See the whole directory tree

</summary>

```
├─ bot/
|  ├─ apis_clients/
|  |  ├─ clash_of_clans.py
|  |  ├─ discord.py
|  |  └─ top_gg.py
|  ├─ core/
|  |  ├─ components/
|  |  |  ├─ buttons/
|  |  |  |  └─ joined_guild_message.py
|  |  |  ├─ select_menus/
|  |  |  |  ├─ auto_roles.py
|  |  |  |  ├─ change_bh_lvl.py
|  |  |  |  ├─ change_clan_super_troops.py
|  |  |  |  ├─ change_player_info_page.py
|  |  |  |  ├─ change_search_clan.py
|  |  |  |  └─ change_th_lvl.py
|  |  ├─ events/
|  |  |  ├─ guild/
|  |  |  |  ├─ guild_join.py
|  |  |  |  └─ guild_remove.py
|  |  |  ├─ member/
|  |  |  |  ├─ member_join.py
|  |  |  |  └─ member_remove.py
|  |  |  ├─ message/
|  |  |  |  └─ message.py
|  |  |  ├─ ready/
|  |  |  |  └─ ready.py
|  |  ├─ slash_commands/
|  |  |  ├─ bot_creators_only/
|  |  |  |  ├─ add_a_bot_id.py
|  |  |  |  ├─ add_reaction_with_id.py
|  |  |  |  ├─ delete_messages.py
|  |  |  |  ├─ download_emojis.py
|  |  |  |  ├─ find_user_by_id.py
|  |  |  |  ├─ reboot.py
|  |  |  |  ├─ refresh_dbl.py
|  |  |  |  ├─ servers_list.py
|  |  |  |  └─ stats.py
|  |  |  ├─ army_link_analyze.py
|  |  |  ├─ auto_roles.py
|  |  |  ├─ bot_info.py
|  |  |  ├─ buildings_bh.py
|  |  |  ├─ buildings_th.py
|  |  |  ├─ clan_current_war.py
|  |  |  ├─ clan_donations.py
|  |  |  ├─ clan_info.py
|  |  |  ├─ clan_members.py
|  |  |  ├─ clan_super_troops.py
|  |  |  ├─ credits.py
|  |  |  ├─ help.py
|  |  |  ├─ link_coc_account.py
|  |  |  ├─ member_info.py
|  |  |  ├─ player_info.py
|  |  |  └─ search_clan.py
|  ├─ bot.py
|  ├─ config.json
|  ├─ emojis.py
|  └─ functions.py
├─ data/
|  ├─ data_source/
|  |  ├─ clash_of_clans.sqlite
|  |  ├─ ids.json
|  |  ├─ required_permissions.json
|  |  └─ useful.json
|  ├─ clash_of_clans.py
|  ├─ config.py
|  ├─ required_permissions.py
|  ├─ secure_folder.py
|  ├─ useful.py
|  └─ views.py
├─ ressources/
|  ├─ supercell_magic_webfont.ttf
|  └─ welcome.png
├─ secure_folder_template/
|  ├─ linked_accounts.json
|  ├─ login.json
|  ├─ secure.sqlite
|  └─ votes.json
├─ CODE_OF_CONDUCT.md
├─ Commands.md
├─ Emojis.zip
├─ FUNDING.yml
├─ LICENSE.md
├─ PRIVACY.md
├─ README.md
├─ TERMS.md
├─ main.py
└─ requirements.txt
```

</details>

The first time you use the bot, please wait that "The bot is ready to be used!" is printed. Else, some things like slash commands could not work.


## Features

You can see [here](Commands.md) the list of available commands.


## Support

You can support this project by subscribing our [Patreon](https://www.patreon.com/clash_info)


## License

Distributed under the [MIT License](LICENSE.md).

[![GitHub](https://img.shields.io/github/license/rreemmii-dev/Clash-Of-Clans-Discord-Bot?label=License)](LICENSE.md)


---

Discord: [RREEMMII#7368](https://discord.com/channels/@me/490190727612071939)
