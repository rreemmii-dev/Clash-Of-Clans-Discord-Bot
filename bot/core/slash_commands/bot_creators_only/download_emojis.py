import os
import shutil

import discord
import requests


async def download_emojis(interaction: discord.Interaction, recreate_emojis_zip: bool):
    if recreate_emojis_zip:
        await interaction.response.defer()
        if os.path.exists("emojis_save"):
            shutil.rmtree("emojis_save")
        os.mkdir("emojis_save")
        for emoji in await interaction.client.fetch_application_emojis():
            r = requests.get(emoji.url, allow_redirects=True)
            extension = r.headers["Content-type"].split("/")[1]
            open(f"emojis_save/{emoji.name}.{extension}", "wb").write(r.content)
        shutil.make_archive("Emojis", "zip", "emojis_save")
        shutil.rmtree("emojis_save")

    file = discord.File(fp="Emojis.zip", filename="Emojis.zip")
    await interaction.followup.send("Here are the emojis !", file=file)
    return
