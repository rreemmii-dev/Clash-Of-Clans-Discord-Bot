import discord

from bot.bot import Bot
from data.config import Config
from data.secure_folder import Login
from data.useful import Ids


intents = discord.Intents.default()
intents.members = True  # Members Intent is required!
if Config["message_content_intent"]:
    intents.message_content = True
Clash_info = Bot(intents=intents)

if Config["main_bot"]:
    Discord_token = Login["discord"]["main"]
    Clash_info.id = Ids["Bot"]
else:
    Discord_token = Login["discord"]["beta"]
    Clash_info.id = Ids["Bot_beta"]
