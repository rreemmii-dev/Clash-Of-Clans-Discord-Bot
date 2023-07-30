import discord


async def delete_message(interaction: discord.Interaction, channel_id: int, number: int):
    channel = interaction.client.get_channel(channel_id)
    if not channel.permissions_for(channel.guild.me).manage_messages:
        await interaction.response.send_message("The bot doesn't have the permission to delete messages")
        return
    await interaction.response.defer()
    async for message in channel.history(limit=number):
        if not message.pinned:
            await message.delete()
    await interaction.followup.send(f"Done\n{channel.jump_url}")
    return
