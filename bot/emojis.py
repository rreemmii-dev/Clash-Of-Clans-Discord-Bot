import discord

from data.config import Config
from data.secure_folder import Login
from data.useful import Useful


Emojis = {}


class EmojisBot(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())

    async def on_ready(self):
        emojis = {}

        emojis_list = await self.fetch_application_emojis()

        th_emojis = {}
        for i in range(1, Useful["max_th_lvl"] + 1):
            th_emojis[i] = discord.utils.get(emojis_list, name=f"TH_{i:02d}")
        emojis["th_emojis"] = th_emojis

        bh_emojis = {}
        for i in range(1, Useful["max_bh_lvl"] + 1):
            bh_emojis[i] = discord.utils.get(emojis_list, name=f"BH_{i:02d}")
        emojis["bh_emojis"] = bh_emojis

        league_emojis = {}
        for league in Useful["league_trophies"].keys():
            emoji = discord.utils.get(emojis_list, name=league.replace(" ", "_").lower())
            league_emojis[league] = emoji
        emojis["league_emojis"] = league_emojis

        builder_league_emojis = {}
        for league in Useful["builder_league_trophies"].keys():
            emoji = discord.utils.get(emojis_list, name=league.replace(" ", "_").lower())
            builder_league_emojis[league] = emoji
        emojis["builder_league_emojis"] = builder_league_emojis

        emojis["troop"] = discord.utils.get(emojis_list, name="TE1")
        troops_emojis = {}
        emoji_to_name = {"TE1": "Barbarian", "TE2": "Archer", "TE3": "Giant", "TE4": "Goblin", "TE5": "Wall Breaker", "TE6": "Balloon", "TE7": "Wizard", "TE8": "Healer", "TE9": "Dragon", "TE10": "P.E.K.K.A", "TE11": "Baby Dragon", "TE12": "Miner", "TE13": "Electro Dragon", "TE14": "Yeti", "TE15": "Dragon Rider", "TE16": "Electro Titan", "TE17": "Root Rider", "TE18": "Thrower", "TD1": "Minion", "TD2": "Hog Rider", "TD3": "Valkyrie", "TD4": "Golem", "TD5": "Witch", "TD6": "Lava Hound", "TD7": "Bowler", "TD8": "Ice Golem", "TD9": "Headhunter", "TD10": "Apprentice Warden", "TD11": "Druid", "SE1": "Lightning Spell", "SE2": "Healing Spell", "SE3": "Rage Spell", "SE4": "Jump Spell", "SE5": "Freeze Spell", "SE6": "Clone Spell", "SE7": "Invisibility Spell", "SE8": "Recall Spell", "SE9": "Revive Spell", "SD1": "Poison Spell", "SD2": "Earthquake Spell", "SD3": "Haste Spell", "SD4": "Skeleton Spell", "SD5": "Bat Spell", "SD6": "Overgrowth Spell"}
        for emoji_name, name in emoji_to_name.items():
            troops_emojis[name] = discord.utils.get(emojis_list, name=emoji_name)
        emojis["troops_emojis"] = troops_emojis

        emoji_to_name = {"ST1": "Super Barbarian", "ST2": "Super Archer", "ST3": "Super Giant", "ST4": "Sneaky Goblin", "ST5": "Super Wall Breaker", "ST6": "Rocket Balloon", "ST7": "Super Wizard", "ST8": "Super Dragon", "ST9": "Inferno Dragon", "ST10": "Super Minion", "ST11": "Super Valkyrie", "ST12": "Super Witch", "ST13": "Ice Hound", "ST14": "Super Bowler", "ST15": "Super Miner", "ST16": "Super Hog Rider"}
        troops_emojis = emojis["troops_emojis"]
        for emoji_name, name in emoji_to_name.items():
            troops_emojis[name] = discord.utils.get(emojis_list, name=emoji_name)
        emojis["troops_emojis"] = troops_emojis

        emoji_to_name = {"P1": "L.A.S.S.I", "P2": "Electro Owl", "P3": "Mighty Yak", "P4": "Unicorn", "P5": "Frosty", "P6": "Diggy", "P7": "Poison Lizard", "P8": "Phoenix", "P9": "Spirit Fox", "P10": "Angry Jelly", "M1": "Wall Wrecker", "M2": "Battle Blimp", "M3": "Stone Slammer", "M4": "Siege Barracks", "M5": "Log Launcher", "M6": "Flame Flinger", "M7": "Battle Drill", "M8": "Troop Launcher"}
        troops_emojis = emojis["troops_emojis"]
        for emoji_name, name in emoji_to_name.items():
            troops_emojis[name] = discord.utils.get(emojis_list, name=emoji_name)
        emojis["troops_emojis"] = troops_emojis

        emojis["barbarian_king"] = discord.utils.get(emojis_list, name="barbarian_king")
        emojis["archer_queen"] = discord.utils.get(emojis_list, name="archer_queen")
        emojis["minion_prince"] = discord.utils.get(emojis_list, name="minion_prince")
        emojis["grand_warden"] = discord.utils.get(emojis_list, name="grand_warden")
        emojis["royal_champion"] = discord.utils.get(emojis_list, name="royal_champion")
        emojis["battle_machine"] = discord.utils.get(emojis_list, name="battle_machine")
        emojis["battle_copter"] = discord.utils.get(emojis_list, name="battle_copter")

        # ----- COC Clans related -----
        war_leagues_emojis = {}
        name_to_emoji_name = {"Unranked": "unranked", "Bronze League III": "bronze_league_III", "Bronze League II": "bronze_league_II", "Bronze League I": "bronze_league_I", "Silver League III": "silver_league_III", "Silver League II": "silver_league_II", "Silver League I": "silver_league_I", "Gold League III": "gold_league_III", "Gold League II": "gold_league_II", "Gold League I": "gold_league_I", "Crystal League III": "crystal_league_III", "Crystal League II": "crystal_league_II", "Crystal League I": "crystal_league_I", "Master League III": "master_league_III", "Master League II": "master_league_II", "Master League I": "master_league_I", "Champion League III": "champion_league_III", "Champion League II": "champion_league_II", "Champion League I": "champion_league_I"}
        for name, emoji_name in name_to_emoji_name.items():
            war_leagues_emojis[name] = discord.utils.get(emojis_list, name=emoji_name)
        emojis["war_leagues"] = war_leagues_emojis

        # ----- COC Remains -----
        emojis["capital_gold"] = discord.utils.get(emojis_list, name="capital_gold")
        emojis["exp"] = discord.utils.get(emojis_list, name="exp")
        emojis["star"] = discord.utils.get(emojis_list, name="star")
        emojis["star_empty"] = discord.utils.get(emojis_list, name="star_empty")  # NOT USED
        emojis["star_old"] = discord.utils.get(emojis_list, name="star_old")  # NOT USED
        emojis["star_success"] = discord.utils.get(emojis_list, name="star_success")
        emojis["trophy"] = discord.utils.get(emojis_list, name="trophy")
        emojis["versus_trophy"] = discord.utils.get(emojis_list, name="versus_trophy")

        # ----- Discord Main -----
        emojis["add_reaction"] = discord.utils.get(emojis_list, name="add_reaction")  # NOT USED
        emojis["channel"] = discord.utils.get(emojis_list, name="channel")  # NOT USED
        emojis["channel_locked"] = discord.utils.get(emojis_list, name="channel_locked")  # NOT USED
        emojis["channel_nsfw"] = discord.utils.get(emojis_list, name="channel_nsfw")  # NOT USED
        emojis["cursor"] = discord.utils.get(emojis_list, name="cursor")  # NOT USED
        emojis["deafened"] = discord.utils.get(emojis_list, name="deafened")  # NOT USED
        emojis["discord"] = discord.utils.get(emojis_list, name="discord")
        emojis["discord_white"] = discord.utils.get(emojis_list, name="discord_white")
        emojis["emoji_ghost"] = discord.utils.get(emojis_list, name="emoji_ghost")  # NOT USED
        emojis["invite"] = discord.utils.get(emojis_list, name="invite")
        emojis["member"] = discord.utils.get(emojis_list, name="member")
        emojis["members"] = discord.utils.get(emojis_list, name="members")
        emojis["mention"] = discord.utils.get(emojis_list, name="mention")  # NOT USED
        emojis["muted"] = discord.utils.get(emojis_list, name="muted")  # NOT USED
        emojis["news"] = discord.utils.get(emojis_list, name="news")
        emojis["nitro"] = discord.utils.get(emojis_list, name="nitro")  # NOT USED
        emojis["owner"] = discord.utils.get(emojis_list, name="owner")
        emojis["pin"] = discord.utils.get(emojis_list, name="pin")
        emojis["pin_unread"] = discord.utils.get(emojis_list, name="pin_unread")  # NOT USED
        emojis["settings"] = discord.utils.get(emojis_list, name="settings")
        emojis["slowmode"] = discord.utils.get(emojis_list, name="slowmode")  # NOT USED
        emojis["stream"] = discord.utils.get(emojis_list, name="stream")  # NOT USED
        emojis["store_tag"] = discord.utils.get(emojis_list, name="store_tag")  # NOT USED
        emojis["typing"] = discord.utils.get(emojis_list, name="typing")  # NOT USED
        emojis["typing_status"] = discord.utils.get(emojis_list, name="typing_status")  # NOT USED
        emojis["undeafened"] = discord.utils.get(emojis_list, name="undeafened")  # NOT USED
        emojis["unmuted"] = discord.utils.get(emojis_list, name="unmuted")  # NOT USED
        emojis["update"] = discord.utils.get(emojis_list, name="update")  # NOT USED
        emojis["updating"] = discord.utils.get(emojis_list, name="updating")  # NOT USED
        emojis["voice"] = discord.utils.get(emojis_list, name="voice")  # NOT USED
        emojis["voice_locked"] = discord.utils.get(emojis_list, name="voice_locked")  # NOT USED

        # ----- General remains -----
        fr_emoji = discord.utils.get(emojis_list, name="fr")  # NOT USED
        us_uk_emoji = discord.utils.get(emojis_list, name="us_uk")  # NOT USED
        emojis["languages_emojis"] = {"English": us_uk_emoji, "French": fr_emoji}  # NOT USED

        emojis["clash_info"] = discord.utils.get(emojis_list, name="Clash_INFO")
        emojis["github"] = discord.utils.get(emojis_list, name="github")

        emojis["yes"] = discord.utils.get(emojis_list, name="yes")
        emojis["no"] = discord.utils.get(emojis_list, name="no")
        emojis["maybe"] = discord.utils.get(emojis_list, name="maybe")

        emojis["calendar"] = discord.utils.get(emojis_list, name="calendar")
        emojis["delete"] = discord.utils.get(emojis_list, name="delete")
        emojis["delete_grey"] = discord.utils.get(emojis_list, name="delete_grey")
        emojis["description"] = discord.utils.get(emojis_list, name="description")
        emojis["donations"] = discord.utils.get(emojis_list, name="donations")
        emojis["id"] = discord.utils.get(emojis_list, name="id")
        emojis["language"] = discord.utils.get(emojis_list, name="language")
        emojis["received"] = discord.utils.get(emojis_list, name="received")

        global Emojis
        Emojis = emojis

        # import os
        # base_path = "C:\\Users\\Remi\\Downloads\\Emojis"
        # folders = os.listdir(base_path)
        # e = [e.name for e in await self.fetch_application_emojis()]
        # for folder in folders:
        #     files = os.listdir(base_path + "\\" + folder)
        #     for file in files:
        #         with open(base_path + "\\" + folder + "\\" + file, 'rb') as textfile:
        #             bytestring = textfile.read()
        #             file = file.replace(".png", "")
        #             file = file.replace(".gif", "")
        #             print(file)
        #             if file not in e:
        #                 await self.create_application_emoji(name=file, image=bytestring)
        await self.close()


client = EmojisBot()
if Config["main_bot"]:
    discord_token = Login["discord"]["main"]
else:
    discord_token = Login["discord"]["beta"]
client.run(discord_token)
