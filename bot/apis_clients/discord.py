import discord

from bot.bot import Bot
from data.config import Config
from data.secure_folder import Login
from data.useful import Ids


intents = discord.Intents.default()
intents.members = True  # Members Intent is required!
Clash_info = Bot(intents=intents)

if Config["main_bot"]:
    Discord_token = Login["discord"]["main"]
    Clash_info.id = Ids["bot"]
else:
    Discord_token = Login["discord"]["beta"]
    Clash_info.id = Ids["bot_beta"]
