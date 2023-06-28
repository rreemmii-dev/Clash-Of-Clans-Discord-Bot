from typing import Union

import coc
import discord

from bot.emojis import Emojis
from data.useful import Useful


def create_embed(title: str, description: str, colour: Union[hex, discord.Colour], footer: str, icon_url: str, img: str = "") -> discord.Embed:
    embed = discord.Embed()
    embed.title = title
    embed.description = description
    embed.colour = colour
    embed.set_footer(text=footer, icon_url=icon_url)
    if img:
        embed.set_image(url=img)
    return embed


def escape_markdown(text: str) -> str:
    text = text.replace("\\", "\\\\")
    text = text.replace("*", "\*")
    text = text.replace("_", "\_")
    text = text.replace("~", "\~")
    text = text.replace(">", "\>")
    text = text.replace("|", "\|")
    text = text.replace("`", "\`")
    text = text.replace(":", "\:")
    return text


def cardinal_to_ordinal_number(n: int) -> str:
    if 10 <= n % 100 < 20:
        ordinal_indicator = "th"
    elif n % 10 == 1:
        ordinal_indicator = "st"
    elif n % 10 == 2:
        ordinal_indicator = "nd"
    elif n % 10 == 3:
        ordinal_indicator = "rd"
    else:
        ordinal_indicator = "th"
    return str(n) + ordinal_indicator


def coc_timestamp_to_timestamp(t: coc.Timestamp) -> int:
    return int(t.time.timestamp())


def trophies_to_league(trophies: int) -> discord.Emoji:
    league_to_trophies = Useful["league_trophies"]
    for league in sorted(league_to_trophies, key=league_to_trophies.get, reverse=True):
        if trophies >= league_to_trophies[league]:
            return Emojis["League_emojis"][league]
