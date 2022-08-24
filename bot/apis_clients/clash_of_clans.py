import coc

from data.config import Config
from data.secure_folder import Login


if Config["main_bot"]:
    login = Login["clash_of_clans"]["main"]
else:
    login = Login["clash_of_clans"]["beta"]

Clash_of_clans = coc.Client(key_names="Discord Bot", key_count=10, load_game_data=coc.LoadGameData(default=True))
