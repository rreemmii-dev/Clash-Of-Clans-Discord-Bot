import discord

from bot.emojis import Emojis
from bot.functions import create_embed, escape_markdown


async def help(interaction: discord.Interaction):
    embed = create_embed("Help: Slash commands list", "", interaction.guild.me.color, "", interaction.guild.me.display_avatar.url)
    embed.add_field(name="Slash Commands list", value="**You can get the bot commands list with detailed description [here](https://rreemmii-dev.github.io/clash-info/commands)**\n\nHowever, here is the list of slash commands:\n" + escape_markdown("/auto_roles_[th|bh|leagues]\n/buildings_[th|bh]\n/player_info\n/clan_info\n/search_clan\n/clan_members\n/clan_donations\n/clan_current_war\n/clan_super_troops\n/army_link_analyze\n/link_coc_account\n/unlink_coc_account\n/member_info\n/bot_info\n/credits"), inline=True)
    embed.add_field(name="Links:", value=f"[{Emojis['clash_info']} Add the bot](https://rreemmii-dev.github.io/clash-info/invite) | [{Emojis['discord']} Support server](https://discord.gg/KQmstPw) | [{Emojis['github']} GitHub](https://github.com/rreemmii-dev/Clash-Of-Clans-Discord-Bot) | [{Emojis['patreon']} Patreon](https://www.patreon.com/clash_info)", inline=False)
    await interaction.response.send_message(embed=embed)
    return
