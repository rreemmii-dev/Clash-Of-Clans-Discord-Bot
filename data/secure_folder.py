import json

from data.config import Config


login_file = open(f"{Config['secure_folder_path']}login.json", "r")
Login = json.load(login_file)
login_file.close()

linked_accounts_file = open(f"{Config['secure_folder_path']}linked_accounts.json", "r")
linked_accounts_raw = json.load(linked_accounts_file)
linked_accounts_file.close()
Linked_accounts = {}
for member_id, tag in linked_accounts_raw.items():
    Linked_accounts[int(member_id)] = tag

votes_file = open(f"{Config['secure_folder_path']}votes.json", "r")
votes_raw = json.load(votes_file)
votes_file.close()
Votes = {}
for member_id, points in votes_raw.items():
    Votes[int(member_id)] = points
