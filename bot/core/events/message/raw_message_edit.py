import datetime

import discord

from bot.functions import create_embed
from data.config import Config
from data.secure_folder import Login
from data.useful import Ids


async def raw_message_edit(self: discord.Client, payload: discord.RawMessageUpdateEvent):
    if not Config["message_content_intent"]:
        return

    # ----- Auto Moderation -----
    if payload.guild_id == Ids["Support_server"]:
        async for message in self.get_guild(Ids["Support_server"]).get_channel(payload.channel_id).history(limit=None):
            if message.id == payload.message_id:
                break
        else:
            message = None
        if message is None:
            return
        author = message.author
        if author is None or type(author) is not discord.Member:
            return
        if author.top_role < message.guild.get_role(Ids["Staff_role"]):
            text = message.content

            if Config["perspective_api"]:
                import googleapiclient
                from googleapiclient import discovery, errors

                client = googleapiclient.discovery.build(
                    "commentanalyzer",
                    "v1alpha1",
                    developerKey=Login["perspective_api"]["token"],
                    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                    static_discovery=False,
                )
                analyze_request = {
                    "comment": {"text": text},
                    "requestedAttributes": {
                        "TOXICITY": {}
                    },
                    "doNotStore": True
                }
                try:
                    response = client.comments().analyze(body=analyze_request).execute()
                    d = {}
                    txt = f"Text: `{text}`\n"
                    for attribute, data in response["attributeScores"].items():
                        d[attribute] = data['spanScores'][0]['score']['value']
                        txt += f"{attribute}: {data['spanScores'][0]['score']['value']} ({data['spanScores'][0]['score']['type']})\n"
                    max_value = (max(d, key=d.get), d[max(d, key=d.get)])
                    if max_value[1] > 0.5:
                        channel = message.guild.get_channel(Ids["Perspective_api_channel"])
                        await channel.send(embed=create_embed(f"{max_value[0]}: {max_value[1]}", f"[This message]({message.jump_url}) with the content: ```{text}``` has been flagged for {max_value[0]} with a probability of {max_value[1]}", message.guild.me.color, "", message.guild.me.display_avatar.url))
                        await message.author.timeout(datetime.timedelta(minutes=5), reason=f"Toxic message:\n{text}")
                        await message.reply(f"{message.author.mention} has been timed out for {max_value[0]}\n\n*This message will be deleted in 5 minutes*", delete_after=300)

                except googleapiclient.errors.HttpError as e:
                    print("Error (PerspectiveApi):", e)
                    pass

            # Test Link
            import re
            pattern = re.compile("""(https?|ftp)://[^\s/$.?#].[^\s]*""", re.IGNORECASE + re.DOTALL)
            if pattern.search(text) is not None:
                await message.author.timeout(datetime.timedelta(minutes=5), reason=f"Link in:\n{text}")
                await message.delete()
                await message.channel.send(f"{message.author.mention} has been timed out for link\n\n*This message will be deleted in 5 minutes*", delete_after=300)

            # Test Discord Invite
            import re
            pattern = re.compile("""discord(?:\.com|app\.com|\.gg)[\/invite\/]?(?:[a-zA-Z0-9\-]{2,32})""", re.IGNORECASE + re.DOTALL)
            if pattern.search(text) is not None:
                await message.author.timeout(datetime.timedelta(minutes=5), reason=f"Link in:\n{text}")
                await message.delete()
                await message.channel.send(f"{message.author.mention} has been timed out for discord invite\n\n*This message will be deleted in 5 minutes*", delete_after=300)
    return
