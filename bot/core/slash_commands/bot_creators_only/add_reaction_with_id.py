import discord


async def add_reaction_with_id(interaction: discord.Interaction, channel_id: int, message_id: int, emoji_id: int):
    channel = interaction.client.get_channel(channel_id)
    async for message in channel.history(limit=None):
        if message.id == message_id:
            emoji = interaction.client.get_emoji(emoji_id)
            await message.add_reaction(emoji)
            await interaction.response.send_message(f"Done\n{message.jump_url}")
            break
    return
