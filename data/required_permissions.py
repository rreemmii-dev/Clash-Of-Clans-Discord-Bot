import json


required_permissions_file = open("data/data_source/required_permissions.json", "r")
Required_permissions = json.load(required_permissions_file)
required_permissions_file.close()
