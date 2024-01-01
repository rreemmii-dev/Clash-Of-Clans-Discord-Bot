import discord

from data.useful import Ids


async def joined_guild_message(interaction: discord.Interaction):
    if interaction.data["custom_id"] == "follow":
        channel = interaction.message.channel
        if interaction.permissions.manage_webhooks:
            if interaction.app_permissions.manage_webhooks:
                news = interaction.client.get_guild(Ids["Support_server"]).get_channel(Ids["News_channel"])
                await news.follow(destination=channel)
                await channel.send("Done!", delete_after=15)
            else:
                await channel.send("The bot cannot do this action !\nPlease give the permission \"Manage Webhooks\" to the bot\n\n*This message will be deleted in 15 seconds*", delete_after=15)
        else:
            await channel.send("You cannot do this action !\nYou are not allowed to manage webhooks.\n\n*This message will be deleted in 15 seconds*", delete_after=15)

    elif interaction.data["custom_id"] == "delete":
        channel = interaction.message.channel
        if interaction.permissions.manage_channels:
            if interaction.app_permissions.manage_channels:
                await channel.delete()
            else:
                await channel.send("The bot cannot do this action !\nPlease give the permission \"Manage Channels\" to the bot\n\n*This message will be deleted in 15 seconds*", delete_after=15)
        else:
            await channel.send("You cannot do this action !\nYou are not allowed to manage channels.\n\n*This message will be deleted in 15 seconds*", delete_after=15)
    return
