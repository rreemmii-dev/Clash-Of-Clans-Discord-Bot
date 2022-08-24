import coc
import discord

from bot.apis_clients.clash_of_clans import Clash_of_clans
from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown, trophies_to_league
from data.views import ComponentView


async def player_info_embed(interaction: discord.Interaction, tag: str, information: str) -> discord.Embed:
    player = await Clash_of_clans.get_player(tag)

    if information == "main":
        lvl_barbarian_king = 0
        lvl_archer_queen = 0
        lvl_grand_warden = 0
        lvl_royal_champion = 0
        lvl_battle_machine = 0
        for hero in player.heroes:
            if hero.name == "Battle Machine":
                lvl_battle_machine = hero.level
            if hero.name == "Barbarian King":
                lvl_barbarian_king = hero.level
            if hero.name == "Archer Queen":
                lvl_archer_queen = hero.level
            if hero.name == "Grand Warden":
                lvl_grand_warden = hero.level
            if hero.name == "Royal Champion":
                lvl_royal_champion = hero.level

        if player.town_hall_weapon:
            weapon = f"({player.town_hall_weapon} {Emojis['Star']})"
        else:
            weapon = ""
        if player.clan:
            clan = f"{escape_markdown(player.clan.name)} ({player.clan.tag})"
        else:
            clan = "None"

        if player.builder_hall:
            player__versus_trophies = player.versus_trophies
            player__best_versus_trophies = player.best_versus_trophies
        else:
            player__versus_trophies = 0
            player__best_versus_trophies = 0
        embed = create_embed(f"Player: {escape_markdown(player.name)} ({player.tag}) (Main information)", f"===== Main Base =====\n{Emojis['Th_emojis'][player.town_hall]} {weapon} | {trophies_to_league(player.trophies)} {player.trophies} | {trophies_to_league(player.best_trophies)} Best: {player.best_trophies} | {Emojis['Exp']} {player.exp_level}\n{Emojis['Barbarian_king']} {lvl_barbarian_king} | {Emojis['Archer_queen']} {lvl_archer_queen} | {Emojis['Grand_warden']} {lvl_grand_warden} | {Emojis['Royal_champion']} {lvl_royal_champion}\n{Emojis['Members']} Clan: {clan}\n{Emojis['Star']} War stars earned: {player.war_stars}\n{Emojis['Capital_gold']} Capital Gold contributed: {player.get_achievement('Most Valuable Clanmate').value: ,}\n{Emojis['Donations']} Troops donated: {player.donations}\n{Emojis['Received']} Troops received: {player.received}\n:crossed_swords: Attacks won: {player.attack_wins}\n:shield: Defenses won: {player.defense_wins}\n\n===== Builder Base =====\n{Emojis['Bh_emojis'][player.builder_hall] if player.builder_hall else Emojis['Bh_emojis'][1]} | {Emojis['Versus_trophy']} {player__versus_trophies} | {Emojis['Versus_trophy']} Best: {player__best_versus_trophies} | {Emojis['Battle_machine']} {lvl_battle_machine}\n:crossed_swords: Versus battle won: {player.versus_attack_wins}\n\n[Open in Clash Of Clans]({player.share_link})", interaction.guild.me.color, f"player_info|{interaction.user.id}", interaction.guild.me.display_avatar.url)

    elif information == "troops":
        troops = {}
        for troop in player.home_troops:
            if not troop.is_super_troop:
                troops[troop.name] = {"name": troop.name, "player": troop.level, "max for the th": troop.get_max_level_for_townhall(player.town_hall), "max for the game": troop.max_level}
        for troop in player.spells:
            troops[troop.name] = {"name": troop.name, "player": troop.level, "max for the th": troop.get_max_level_for_townhall(player.town_hall), "max for the game": troop.max_level}
        for troop in player.siege_machines:
            troops[troop.name] = {"name": troop.name, "player": troop.level, "max for the th": troop.get_max_level_for_townhall(player.town_hall), "max for the game": troop.max_level}
        for troop in player.hero_pets:
            troops[troop.name] = {"name": troop.name, "player": troop.level, "max for the th": 10, "max for the game": troop.max_level}  # TODO : Edit "max for the th" when it will be available
        text = "*level | max level (TH) | max level (all the game)*"

        for troop in troops.values():
            emoji = Emojis["Troops_emojis"][troop["name"]]
            if troop["name"] == "Barbarian":
                text += "\n\n__Troops:__\n"
                a = 0
            if troop["name"] == "Minion":
                text += "\n\n__Dark troops:__\n"
                a = 0
            if troop["name"] == "Lightning Spell":
                text += "\n\n__Spells:__\n"
                a = 0
            if troop["name"] == "Poison Spell":
                text += "\n\n__Dark spells__:\n"
                a = 0
            if troop["name"] == "Wall Wrecker":
                text += "\n\n__Siege machines__:\n"
                a = 0
            if troop["name"] == "L.A.S.S.I":
                text += "\n\n__Pets__:\n"
                a = 0
            if a == 4:
                a = 0
                text += "\n"
            a += 1
            emoji = f"<:{emoji.name}:{emoji.id}>"
            text += f"{emoji}: {troop['player']} | {troop['max for the th']} | {troop['max for the game']} "
        embed = create_embed(f"Player: {escape_markdown(player.name)} ({player.tag}) (Troops)", text, interaction.guild.me.color, f"player_info|{interaction.user.id}", interaction.guild.me.display_avatar.url)

    elif information == "success":
        achievements = "*name: stars | % for next star*"
        total_stars = 0
        for achievement in player.achievements:
            total_stars += achievement.stars
            achievements += f"\n{achievement.name}: {achievement.stars} {Emojis['Star_success']} | {int(achievement.value / achievement.target * 100)}%"
        achievements += f"\n\nTotal stars: {total_stars} {Emojis['Star_success']}"
        embed = create_embed(f"Player: {escape_markdown(player.name)} ({player.tag}) (Achievements)", f"{achievements}\n[Open in Clash Of Clans]({player.share_link})", interaction.guild.me.color, f"player_info|{interaction.user.id}", interaction.guild.me.display_avatar.url)

    return embed


async def player_info(interaction: discord.Interaction, tag: str, information: str):
    try:
        await Clash_of_clans.get_player(tag)
    except coc.errors.NotFound:
        await interaction.response.send_message(f"Player not found\nThere is no player with the tag `{tag}`.", ephemeral=True)
        return
    embed = await player_info_embed(interaction, tag, information)

    await interaction.response.send_message(embed=embed, view=ComponentView("player_info"))
    return
