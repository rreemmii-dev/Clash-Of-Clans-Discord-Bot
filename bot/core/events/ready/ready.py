import datetime
import os
import shutil
import sqlite3
import threading
import time

import discord
from bot.emojis import Emojis
from data.config import Config
from data.useful import Ids


async def ready(self: discord.AutoShardedClient):
    print("Beginning of the preparation of the bot")

    print("Slash Commands will be synced...")
    await self.sync_commands()
    print("Slash Commands synced")

    from bot.apis_clients.clash_of_clans import Clash_of_clans, login
    await Clash_of_clans.login(login["email"], login["password"])

    # for guild in self.guilds:
    #     await guild.chunk()

    if Config["main_bot"]:
        status_channel = self.get_channel(Ids["status_channel"])
        await status_channel.send(f"{Emojis['yes']} Connected `{datetime.datetime.now().replace(microsecond=0).isoformat(sep=' ')}`")

    from bot.apis_clients.discord import Discord_token as discord_token, intents

    def thread_weekly_stats():
        while True:
            date = datetime.datetime.now()
            monday = datetime.date.today() + datetime.timedelta(days=(7 - date.weekday()))
            monday = datetime.datetime(monday.year, monday.month, monday.day)
            diff = monday - date
            time.sleep(diff.seconds + diff.days * 24 * 3600)
            print("Weekly Stats", datetime.datetime.now())

            # ===== WEEKLY STATS =====

            class WeeklyStatsBot(discord.AutoShardedClient):
                def __init__(self):
                    super().__init__(intents=intents, chunk_guilds_at_startup=False)

                async def on_ready(self):
                    channel = self.get_channel(Ids["weekly_stats_channel"])
                    old_servers_count = 0
                    async for message in channel.history(limit=None):
                        if message.is_system():
                            await message.delete()
                        if message.pinned:
                            old_servers_count = int(message.content)
                            await message.delete()
                            break
                    msg = await channel.send(str(len(self.guilds)))
                    await msg.pin()
                    diff_servers_count = len(self.guilds) - old_servers_count
                    diff_servers_count = "%+d" % diff_servers_count
                    await channel.send(f"Evolution of number of servers this week: {diff_servers_count}")
                    await self.close()

            weekly_stats_bot = WeeklyStatsBot()
            weekly_stats_bot.run(discord_token)

    thread = threading.Thread(target=thread_weekly_stats)
    thread.start()

    def thread_monthly_users():
        while True:
            date = datetime.datetime.now()
            if date.month < 12:
                day1 = datetime.datetime(date.year, date.month + 1, 1)
            else:
                day1 = datetime.datetime(date.year + 1, 1, 1)
            diff = day1 - date
            time.sleep(diff.seconds + diff.days * 24 * 3600)
            print("Monthly Users Stats", datetime.datetime.now())

            # ===== MONTHLY USERS =====

            class MonthlyUsersBot(discord.AutoShardedClient):

                def __init__(self):
                    super().__init__(intents=intents, chunk_guilds_at_startup=False)

                async def on_ready(self):
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

                    channel = self.get_channel(Ids["monthly_stats_channel"])
                    await channel.send(text)
                    cursor.execute("DELETE FROM bot_usage")
                    connection.commit()
                    await self.close()

            monthly_users_bot = MonthlyUsersBot()
            monthly_users_bot.run(discord_token)

    thread = threading.Thread(target=thread_monthly_users)
    thread.start()

    def thread_backup_secure_folder():
        while True:
            date = datetime.datetime.now()
            monday = datetime.date.today() + datetime.timedelta(days=(7 - date.weekday()))
            monday = datetime.datetime(monday.year, monday.month, monday.day)
            diff = monday - date
            time.sleep(diff.seconds + diff.days * 24 * 3600)
            print("Save Secure Folder", datetime.datetime.now())

            # ===== BACKUP SECURE FOLDER =====

            class BackupSecureFolderBot(discord.AutoShardedClient):

                def __init__(self):
                    super().__init__(intents=intents, chunk_guilds_at_startup=False)

                async def on_ready(self):
                    shutil.make_archive("Secure Folder", 'zip', Config["secure_folder_path"][:-1])
                    file = discord.File(fp="Secure Folder.zip", filename="Secure Folder.zip")
                    await self.get_channel(Ids["secure_folder_backup_channel"]).send("Here is the Secure Folder backup !", file=file)
                    os.remove("Secure Folder.zip")
                    await self.close()

            secure_folder_backup_bot = BackupSecureFolderBot()
            secure_folder_backup_bot.run(discord_token)

    thread = threading.Thread(target=thread_backup_secure_folder)
    thread.start()

    print("The bot is ready to be used!")

    nb_guilds = len(self.guilds)
    act = discord.Activity(type=discord.ActivityType.watching, name=f"{nb_guilds: ,} servers")
    await self.change_presence(status=discord.Status.online, activity=act)
    return
