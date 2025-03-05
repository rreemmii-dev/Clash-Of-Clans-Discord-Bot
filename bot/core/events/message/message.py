from io import BytesIO

import discord
import requests

from data.useful import Ids


async def on_message(self: discord.AutoShardedClient, message: discord.Message):
    if message.author.bot:
        return
    if message.channel.type is discord.ChannelType.private:
        channel = self.get_channel(Ids["dm_bot_log_channel"])
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
    return
