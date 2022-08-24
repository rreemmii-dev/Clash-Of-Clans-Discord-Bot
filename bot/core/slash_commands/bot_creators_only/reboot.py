import os

import discord


async def reboot(interaction: discord.Interaction):
    await interaction.response.send_message("The Raspberry Pi will be rebooted")
    os.system("sudo reboot")
    return
