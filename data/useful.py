import json


ids_file = open("data/data_source/ids.json", "r")
Ids = json.load(ids_file)
ids_file.close()

useful_file = open("data/data_source/useful.json", "r")
Useful = json.load(useful_file)
useful_file.close()
