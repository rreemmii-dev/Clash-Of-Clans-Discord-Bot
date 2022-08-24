import json


config_file = open("bot/config.json", "r")
Config = json.load(config_file)
config_file.close()
