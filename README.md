# Clash-Of-Clans-Discord-Bot

[![Discord](https://img.shields.io/discord/719537805604290650?color=%230000ff&label=Discord&logo=https%3A%2F%2Fdiscord.com%2Fassets%2F2c21aeda16de354ba5334551a883b481.png&logoColor=%2300000000)](https://discord.gg/KQmstPw)
[![Python version](https://img.shields.io/badge/Python-%E2%89%A5%203.8-blue)](https://www.python.org/downloads/)
[![GitHub Repo stars](https://img.shields.io/github/stars/rreemmii-dev/Clash-Of-Clans-Discord-Bot?label=Stars)](https://github.com/rreemmii-dev/Clash-Of-Clans-Discord-Bot/stargazers)
[![GitHub contributors](https://img.shields.io/github/contributors/rreemmii-dev/Clash-Of-Clans-Discord-Bot?label=Contributors)](https://github.com/rreemmii-dev/Clash-Of-Clans-Discord-Bot/graphs/contributors)

**A Discord Bot about the game Clash of Clans, using the [discord.py](https://github.com/Rapptz/discord.py) and [coc.py](https://github.com/mathsman5133/coc.py) libraries.**

To test the bot, please [add it to your server](https://rreemmii-dev.github.io/clash-info/invite) or join
the [support server](https://discord.gg/KQmstPw).

To ask for help, please join the [support server](https://discord.gg/KQmstPw).

## Table of contents

- [Installation + Setup](#installation--setup)
- [Run](#run)
- [Features](#features)
- [Support](#support)
- [Contribute](#contribute)
- [License](#license)

## Installation + Setup

### Installation

```shell
# Clone the repository:
git clone https://github.com/rreemmii-dev/Clash-Of-Clans-Discord-Bot.git

# Download the required libraries:
pip install -r Clash-Of-Clans-Discord-Bot\requirements.txt
```

### Discord bot creation and setup

1) Create a bot following [these steps](https://discordpy.readthedocs.io/en/latest/discord.html).
2) Invite the bot to your server with the link provided
   by https://discord.com/developers/applications/[your_bot_id]/installation. Add the `bot` and `applications.commands`
   scopes, and the required permissions given [here](data/data_source/useful.json) (or the `administrator` permission).
3) Enable [member privileged intent](https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents).
4) Unzip [Emojis.zip](Emojis.zip), and add all emojis to your
   bot (https://discord.com/developers/applications/[your_bot_id]/emojis).

### Config files setup

#### Fill in the Secure Folder

Rename the [secure_folder_template](secure_folder_template) to "Secure Folder".

Fill in the [Secure Folder/login.json](secure_folder_template/login.json) file with your credentials.

| Field                                        | When is it required?                                    | How to get it?                                                     |
|----------------------------------------------|---------------------------------------------------------|--------------------------------------------------------------------|
| `discord > main`                             | Always Required                                         | Help here: https://discordpy.readthedocs.io/en/latest/discord.html |
| `discord > beta`                             | Used if `main_bot` is set to `false` in bot/config.json | Help here: https://discordpy.readthedocs.io/en/latest/discord.html |
| `clash_of_clans > main > [email / password]` | Always Required                                         | To create an account: https://developer.clashofclans.com           |
| `clash_of_clans > beta > [email / password]` | Used if `main_bot` is set to `false` in bot/config.json | To create an account: https://developer.clashofclans.com           |

#### Edit the [bot/config.json](bot/config.json) file.

| Field                | Description                                         |
|----------------------|-----------------------------------------------------|
| `secure_folder_path` | Relative path to the secure folder (from `main.py`) |
| `main_bot`           | Set it to `false` to run the beta bot for tests.    |

#### Fill in the [data/data_source/ids.json](data/data_source/ids.json) file.

| Field                          | Description                                                                                                                                                                                              |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Users                          |                                                                                                                                                                                                          |
| `creators`                     | List of bot creators ids. Shown in `/credits`                                                                                                                                                            |
| `bot`                          | Main bot id.                                                                                                                                                                                             |
| `bot_beta`                     | Beta bot id.                                                                                                                                                                                             |
| Servers                        |                                                                                                                                                                                                          |
| `bot_creators_only_server`     | The server where all slash commands for bot creators are. Everyone in this server will be able to use slash commands for creators, so make sure only bot creators are in this server.                    |
| Channels                       |                                                                                                                                                                                                          |
| `weekly_stats_channel`         | Where the bot sends a weekly message with servers number evolution.                                                                                                                                      |
| `monthly_stats_channel`        | Where the bot sends a monthly message about its use statistics.                                                                                                                                          |
| `news_channel`                 | The news channel where announcements about the bot are sent. This channel should belong to your support server.                                                                                          |
| `status_channel`               | Where the bot sends a message when it is connected.                                                                                                                                                      |
| `guilds_bot_log_channel`       | Where the bot sends a message when it joins/leaves a server with more than 100 users (bot are not considered as users). For privacy reasons, please create this channel in the bot creators only server. |
| `dm_bot_log_channel`           | The channel with logs of messages sent to the bot by DMs. For privacy reasons, please create this channel in the bot creators only server.                                                               |
| `secure_folder_backup_channel` | Where backups of the Secure Folder are sent every week. For privacy reasons, please create this channel in the bot creators only server.                                                                 |

## Run

```shell
# Run the script:
python Clash-Of-Clans-Discord-Bot\main.py
```

Please wait that "The bot is ready to be used!" is printed before using the bot. Else, things like slash commands could
not work.

## Features

You can see [here](Commands.md) the list of available commands.

Here is the whole directory tree:

```
├─ bot/
|  ├─ apis_clients/
|  |  ├─ clash_of_clans.py
|  |  └─ discord.py
|  ├─ core/
|  |  ├─ components/
|  |  |  ├─ buttons/
|  |  |  |  └─ joined_guild_message.py
|  |  |  ├─ select_menus/
|  |  |  |  ├─ auto_roles.py
|  |  |  |  ├─ change_bh_lvl.py
|  |  |  |  ├─ change_player_info_page.py
|  |  |  |  ├─ change_search_clan.py
|  |  |  |  └─ change_th_lvl.py
|  |  ├─ events/
|  |  |  ├─ guild/
|  |  |  |  ├─ guild_join.py
|  |  |  |  └─ guild_remove.py
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
|  |  |  ├─ player_info.py
|  |  |  ├─ search_clan.py
|  |  |  └─ user_info.py
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
├─ secure_folder_template/
|  ├─ linked_accounts.json
|  ├─ login.json
|  ├─ secure.sqlite
|  └─ votes.json
├─ Commands.md
├─ CONTRIBUTING.md
├─ Emojis.zip
├─ FUNDING.yml
├─ LICENSE.md
├─ PRIVACY.md
├─ README.md
├─ TERMS.md
├─ main.py
└─ requirements.txt
```

## Support

You can support this project by subscribing our [Patreon](https://www.patreon.com/clash_info)

## Contribute

You can help this project by contributing to it. See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## License

Distributed under the [MIT License](LICENSE.md).

[![GitHub](https://img.shields.io/github/license/rreemmii-dev/Clash-Of-Clans-Discord-Bot?label=License)](LICENSE.md)


---

Discord: [RREEMMII#7368](https://discord.com/channels/@me/490190727612071939)
