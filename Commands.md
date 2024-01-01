# Clash INFO Slash Commands

Here is a table with each slash command, its description and its options.

<details>
<summary>Glossary</summary>

- `BH` : Builder Hall
- `TH` : Town Hall

</details>


### `/_help`, `/help`

Show the help message to use Clash INFO

*Options:* None


### `/auto_roles_bh`, `/auto_roles_leagues`, `/auto_roles_th`

Create an auto-roles system to give the [BH level / league / TH level] roles.

The bot needs the `Manage Roles`, `Send Messages`, `View Channels` and `Embed Links` permissions

*Options:* `channel`: Channel where it will be the auto-roles system


### `/buildings_bh`, `/buildings_th`

Show the maximum level for each building at the given [BH / TH] level.

*Options:* `builder_hall_level`, `town_hall_level`


### `/player_info`

Show data about the player

*Options:* `player_tag`: Clash Of Clans player tag, format: #A1B2C3D4, <br>`information`


### `/clan_info`

Show data about the clan

*Options:* `clan_tag`: Clash Of Clans clan tag, format: #A1B2C3D4


### `/search_clan`

Search clans by name

*Options:* `name`: Clan name


### `/clan_members`

Show the clan members.

The bot needs the `Send Messages` and `View Channels` permissions

*Options:* `clan_tag`: Clash Of Clans clan tag, format: #A1B2C3D4


### `/clan_donations`

Show the clan members, sorted by donations stats.

The bot needs the `Send Messages` and `View Channels` permissions

*Options:* `clan_tag`: Clash Of Clans clan tag, format: #A1B2C3D4


### `/clan_current_war`

Show data about the clan war

*Options:* `clan_tag`: Clash Of Clans clan tag, format: #A1B2C3D4


### `/clan_super_troops`

Show which super troop has been activated, and by which player of the clan

*Options:* `clan_tag`: Clash Of Clans clan tag, format: #A1B2C3D4


### `/army_link_analyze`

Show the troops and spells from an in-game army link

*Options:* `army_link`: Army link, gettable from Clash Of Clans > Army > Quick Train > Share > Share as link


### `/link_coc_account`

Link your Clash Of Clans account to your Discord account

*Options:* `player_tag`: Clash Of Clans player tag, format: #A1B2C3D4, <br>`api_token`: Your API token, findable in Clash Of Clans > Settings > More Settings > API Token > Show


### `/unlink_coc_account`

Unlink your Clash Of Clans account from your Discord account

*Options:* `player_tag`: Clash Of Clans player tag, format: #A1B2C3D4


### `/member_info`

Show permissions, when the member joined Discord / the server and their avatar

*Options:* `member`


### `/bot_info`

Show some information about the bot

*Options:* None
