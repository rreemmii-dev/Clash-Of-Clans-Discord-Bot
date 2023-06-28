import asyncio
import datetime
import io
import json
import os
import shutil
import sqlite3
import threading
import time

import discord
import flask
import waitress
from bot.emojis import Emojis
from bot.functions import create_embed
from data.config import Config
from data.secure_folder import Login
from data.useful import Ids


async def ready(self: discord.AutoShardedClient):
    print("Beginning of the preparation of the bot")

    if Config["main_bot"]:
        status_channel = self.get_channel(Ids["Status_channel"])
        await status_channel.send(f"{Emojis['Yes']} Connected `{datetime.datetime.now().replace(microsecond=0).isoformat(sep=' ')}`")

    print("Slash Commands will be synced...")
    await self.sync_commands()
    print("Slash Commands synced")

    from bot.apis_clients.clash_of_clans import Clash_of_clans, login
    await Clash_of_clans.login(login["email"], login["password"])

    for guild in self.guilds:
        await guild.chunk()

    if Config["main_bot"]:
        status_channel = self.get_channel(Ids["Status_channel"])
        await status_channel.send(f"{Emojis['Yes']} Cache loaded `{datetime.datetime.now().replace(microsecond=0).isoformat(sep=' ')}`")

    if Ids["Member_role"]:
        support_server = self.get_guild(Ids["Support_server"])
        member_role = support_server.get_role(Ids["Member_role"])
        for member in support_server.members:
            if member_role not in member.roles and not member.bot:
                await member.add_roles(member_role)

    clash_info = self

    if Config["main_bot"]:
        discord_token = Login["discord"]["main"]
    else:
        discord_token = Login["discord"]["beta"]

    def thread_weekly_stats():
        while True:
            date = datetime.datetime.now()
            monday = datetime.date.today() + datetime.timedelta(days=(7 - date.weekday()))
            monday = datetime.datetime(monday.year, monday.month, monday.day)
            diff = monday - date
            time.sleep(diff.seconds + diff.days * 24 * 3600)
            print("Weekly Stats", datetime.datetime.now())

            # ===== WEEKLY STATS =====

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            class WeeklyStatsBot(discord.AutoShardedClient):
                def __init__(self):
                    super().__init__(intents=discord.Intents.default())

                async def on_ready(self):
                    channel = self.get_channel(Ids["Weekly_stats_channel"])
                    old_servers_count = 0
                    async for message in channel.history(limit=None):
                        if message.is_system():
                            await message.delete()
                        if message.pinned:
                            old_servers_count = int(message.content)
                            await message.delete()
                            break
                    msg = await channel.send(str(len(clash_info.guilds)))
                    await msg.pin()
                    diff_servers_count = len(clash_info.guilds) - old_servers_count
                    diff_servers_count = "%+d" % diff_servers_count
                    await channel.send(f"Evolution of number of servers this week: {diff_servers_count}")
                    await self.close()

            weekly_stats_bot = WeeklyStatsBot()
            try:
                loop.run_until_complete(weekly_stats_bot.start(discord_token))
            except KeyboardInterrupt:
                loop.run_until_complete(weekly_stats_bot.close())
            finally:
                loop.close()

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

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            class MonthlyUsersBot(discord.AutoShardedClient):

                def __init__(self):
                    super().__init__(intents=discord.Intents.default())

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

                    channel = self.get_channel(Ids["Monthly_stats_channel"])
                    await channel.send(text)
                    cursor.execute("DELETE FROM bot_usage")
                    connection.commit()
                    await self.close()

            monthly_users_bot = MonthlyUsersBot()
            try:
                loop.run_until_complete(monthly_users_bot.start(discord_token))
            except KeyboardInterrupt:
                loop.run_until_complete(monthly_users_bot.close())
            finally:
                loop.close()

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

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            class BackupSecureFolderBot(discord.AutoShardedClient):

                def __init__(self):
                    super().__init__(intents=discord.Intents.default())

                async def on_ready(self):
                    shutil.make_archive("Secure Folder", 'zip', Config["secure_folder_path"][:-1])
                    file = discord.File(fp="Secure Folder.zip", filename="Secure Folder.zip")
                    await self.get_channel(Ids["Secure_folder_backup_channel"]).send("Here is the Secure Folder backup !", file=file)
                    os.remove("Secure Folder.zip")
                    await self.close()

            secure_folder_backup_bot = BackupSecureFolderBot()
            try:
                loop.run_until_complete(secure_folder_backup_bot.start(discord_token))
            except KeyboardInterrupt:
                loop.run_until_complete(secure_folder_backup_bot.close())
            finally:
                loop.close()

    thread = threading.Thread(target=thread_backup_secure_folder)
    thread.start()

    def thread_webhooks_app():
        app = flask.Flask(__name__)

        @app.route("/topgg_webhook", methods=["post"])
        def topgg_webhook():
            if flask.request.remote_addr != "159.203.105.187" or "Authorization" not in flask.request.headers.keys() or flask.request.headers["Authorization"] != Login["top_gg"]["authorization"]:
                authorization = None if "Authorization" not in flask.request.headers.keys() else flask.request.headers["Authorization"]
                print(f"Unauthorized:\nIP = {flask.request.remote_addr}\nAuthorization = {authorization}")
                return flask.Response(status=401)

            def run_bot(voter_id: int):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                class TopggWebhooksBot(discord.AutoShardedClient):
                    def __init__(self):
                        super().__init__(intents=discord.Intents.default())

                    async def on_ready(self):
                        from data.secure_folder import Votes

                        user = clash_info.get_user(voter_id)
                        votes_channel = self.get_channel(Ids["Votes_channel"])

                        if user.id not in Votes.keys():
                            Votes[user.id] = 1
                        else:
                            Votes[user.id] += 1
                        json_text = json.dumps(Votes, sort_keys=True, indent=4)
                        def_votes = open(f"{Config['secure_folder_path']}votes.json", "w")
                        def_votes.write(json_text)
                        def_votes.close()
                        vote_copy = dict(Votes)
                        vote = {}
                        for member_id, member_votes in vote_copy.items():
                            member = clash_info.get_user(int(member_id))
                            vote[member.mention] = member_votes
                        vote = sorted(vote.items(), key=lambda t: t[1])
                        text = ""
                        for user_vote_tuple in vote:
                            text += f"{user_vote_tuple[0]} has voted {user_vote_tuple[1]} times\n"
                        embed = create_embed(f"{user} has voted for Clash INFO", text, votes_channel.guild.me.color, "", votes_channel.guild.me.display_avatar.url)
                        await votes_channel.send(embed=embed)
                        await self.close()

                topgg_webhooks_bot = TopggWebhooksBot()
                try:
                    loop.run_until_complete(topgg_webhooks_bot.start(discord_token))
                except KeyboardInterrupt:
                    loop.run_until_complete(topgg_webhooks_bot.close())
                finally:
                    loop.close()

            thread = threading.Thread(target=run_bot, kwargs={"voter_id": int(flask.request.get_json()["user"])})
            thread.start()
            return flask.Response(status=200)

        @app.route("/github_webhook", methods=["post"])
        def github_webhook():
            if flask.request.get_json()["repository"]["name"] != "Clash-Of-Clans-Discord-Bot":
                return 418

            def run_bot(event_name: str, original_json: dict):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                class GitHubWebhooksBot(discord.AutoShardedClient):
                    def __init__(self):
                        super().__init__(intents=discord.Intents.default())

                    async def on_ready(self):
                        events_channel = self.get_channel(Ids["Events_github_channel"])
                        embed = create_embed(f"{event_name.capitalize()} by {original_json['sender']['login']}", "", events_channel.guild.me.color, "", events_channel.guild.me.display_avatar.url)
                        description = ""
                        if event_name == "push":
                            description += f"[{'Forced ' if original_json['forced'] else ''}Push]({original_json['head_commit']['url']}) by [{original_json['sender']['login']}]({original_json['sender']['html_url']})\n"
                            description += f"{original_json['head_commit']['message']}\n\n"
                            nl = "\n"  # Because `f"{'\n'}"` is forbidden
                            if json.dumps(original_json['head_commit']['added']):
                                description += f"**Added:**\n{nl.join(original_json['head_commit']['added'])}\n\n"
                            if json.dumps(original_json['head_commit']['modified']):
                                description += f"**Modified:**\n{nl.join(original_json['head_commit']['modified'])}\n\n"
                            if json.dumps(original_json['head_commit']['removed']):
                                description += f"**Removed:**\n{nl.join(original_json['head_commit']['removed'])}\n\n"
                        elif event_name == "fork":
                            description += f"[Fork]({original_json['forkee']['html_url']}) by [{original_json['sender']['login']}]({original_json['sender']['html_url']})\n"
                        elif event_name == "star":
                            if original_json['action'] == 'created':
                                from bot.functions import cardinal_to_ordinal_number
                                description += f"[{original_json['sender']['login']}]({original_json['sender']['html_url']}) is now the {cardinal_to_ordinal_number(original_json['repository']['stargazers_count'])} stargazer!\n[See the stargazers list]({original_json['repository']['html_url']}/stargazers)"
                            else:
                                description += f"[{original_json['sender']['login']}]({original_json['sender']['html_url']}) is no longer a stargazer.\n[See the stargazers list]({original_json['repository']['html_url']}/stargazers)"
                        elif event_name == "":  # TODO : Add other event types
                            pass
                        embed.description = description
                        await events_channel.send(f"{event_name.capitalize()} by {original_json['sender']['login']}")

                        file_content = io.BytesIO(json.dumps(original_json, indent=4).encode('utf-8'))
                        file = discord.File(file_content, filename="content.json")
                        await events_channel.send(embed=embed, file=file)
                        await self.close()

                github_webhooks_bot = GitHubWebhooksBot()
                try:
                    loop.run_until_complete(github_webhooks_bot.start(discord_token))
                except KeyboardInterrupt:
                    loop.run_until_complete(github_webhooks_bot.close())
                finally:
                    loop.close()

            thread = threading.Thread(target=run_bot, kwargs={"event_name": flask.request.headers["X-Github-Event"], "original_json": flask.request.get_json()})
            thread.start()
            return flask.Response(status=200)

        waitress.serve(app, host="0.0.0.0", port=8080)

    thread = threading.Thread(target=thread_webhooks_app, args=())
    thread.start()

    print("The bot is ready to be used!")

    nb_guilds = len(self.guilds)
    act = discord.Activity(type=discord.ActivityType.watching, name=f"{nb_guilds: ,} servers")
    await self.change_presence(status=discord.Status.online, activity=act)
    return
