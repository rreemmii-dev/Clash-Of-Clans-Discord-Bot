import os
import shutil

import discord
import requests

from data.useful import Ids


async def download_emojis(interaction: discord.Interaction, recreate_emojis_zip: bool):
    if recreate_emojis_zip:
        await interaction.response.defer()
        if os.path.exists("Emojis_save"):
            shutil.rmtree("Emojis_save")
        os.mkdir("Emojis_save")
        emojis_servers_id = [Ids["Emojis_coc_players_related_server"], Ids["Emojis_coc_troops_server"], Ids["Emojis_coc_clans_related_server"], Ids["Emojis_coc_remains_server"], Ids["Emojis_discord_main_server"], Ids["Emojis_general_remains_server"]]
        forbidden_characters = ["<", ">", ":", "“", "/", "\\", "|", "?", "*"]
        for guild_id in emojis_servers_id:
            guild = interaction.client.get_guild(guild_id)
            guild_name = guild.name
            for char in forbidden_characters:
                guild_name = guild_name.replace(char, "-")
            os.mkdir(f"Emojis_save/{guild_name}")
            for emoji in guild.emojis:
                r = requests.get(emoji.url, allow_redirects=True)
                extension = r.headers["Content-type"].split("/")[1]
                open(f"Emojis_save/{guild_name}/{emoji.name}.{extension}", "wb").write(r.content)
        shutil.make_archive("Emojis", "zip", "Emojis_save")
        shutil.rmtree("Emojis_save")

    file = discord.File(fp="Emojis.zip", filename="Emojis.zip")
    await interaction.followup.send("Here are the emojis !", file=file)
    return
