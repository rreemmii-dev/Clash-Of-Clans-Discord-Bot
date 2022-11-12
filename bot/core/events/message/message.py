from io import BytesIO

import discord
import requests

from bot.functions import create_embed
from data.config import Config
from data.useful import Ids


async def on_message(self: discord.AutoShardedClient, message: discord.Message):
    if message.author.bot:
        return
    if message.channel.type is discord.ChannelType.private:
        channel = self.get_channel(Ids["Dm_bot_log_channel"])
        if message.author.id != self.id:
            await message.author.send("Hello !\nI am a bot, so I cannot answer you !\nSupport server:\nhttps://discord.gg/KQmstPw")
            if len(message.attachments) == 0:
                await channel.send(f"```{message.content}``` from:\n{message.author} (`{message.author.id}`)\nMessage_id: `{message.id}`")
            else:
                files = []
                for attachment in message.attachments:
                    response = requests.get(attachment.url)
                    img = BytesIO(response.content)
                    files += [discord.File(img, filename=f"file.{response.headers['Content-Type'].split('/')[1]}")]
                    if message.content == "":
                        message.content = " "
                await channel.send(f"```{message.content}``` from:\n{message.author} (`{message.author.id}`)\nMessage_id: `{message.id}`", files=files)
        return

    if not Config["message_content_intent"]:
        return

    if message.author.id in Ids["Creators"]:
        if message.content.startswith("dltmsg") and message.channel.permissions_for(message.author).manage_messages:
            number = int(message.content.split(" ")[1])
            message_numbers = 0
            async for msg in message.channel.history(limit=number + 1):
                if not msg.pinned:
                    message_numbers += 1
                    await msg.delete()
            message_numbers -= 1
            embed = create_embed("Messages deleted", f"{message_numbers: ,} messages deleted", message.guild.me.color, "", message.guild.me.display_avatar.url)
            msg = await message.channel.send(embed=embed)
            import asyncio
            await asyncio.sleep(10)
            await msg.delete()
            return
    return
