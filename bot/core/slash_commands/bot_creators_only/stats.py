import sqlite3

import discord

from bot.functions import create_embed
from data.config import Config


async def stats(interaction: discord.Interaction):
    connection = sqlite3.connect(Config["secure_folder_path"] + "secure.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM bot_usage")
    nb_monthly_users = cursor.fetchone()[0]
    text = f"**Monthly users: {nb_monthly_users}\n\n**"
    commands_stats = {}

    cursor.execute("PRAGMA table_info(bot_usage)")
    commands_names = []
    for command in cursor.fetchall():
        command_name = command[1]
        if command_name != "user_id":
            commands_names += [command_name]

    for command_name in commands_names:
        cursor.execute(f"SELECT COUNT(*) FROM bot_usage WHERE NOT {command_name} = 0")
        commands_stats[command_name] = cursor.fetchone()[0]

    for name, usages in {k: v for k, v in sorted(commands_stats.items(), key=lambda x: x[1], reverse=True)}.items():
        text += f"{name}: {usages}\n"

    embed = create_embed("Stats:", text, interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    await interaction.response.send_message(embed=embed)
    return
