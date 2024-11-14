import sqlite3

from data.useful import Useful


connection = sqlite3.connect("data/data_source/clash_of_clans.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

Builder_base_buildings = {}
for lvl in range(1, Useful["max_bh_lvl"] + 1):
    Builder_base_buildings[lvl] = {}
    for category in Useful["bh_buildings_categories"]:
        Builder_base_buildings[lvl][category] = {}
        cursor.execute(f"SELECT name, BH{lvl} FROM builder_base_buildings WHERE category='{category}' AND BH{lvl}!=0")
        for building in cursor.fetchall():
            Builder_base_buildings[lvl][category][building["name"]] = building[f"BH{lvl}"]

Main_base_buildings = {}
for lvl in range(1, Useful["max_th_lvl"] + 1):
    Main_base_buildings[lvl] = {}
    for category in Useful["th_buildings_categories"]:
        Main_base_buildings[lvl][category] = {}
        cursor.execute(f"SELECT name, TH{lvl} FROM main_base_buildings WHERE category='{category}' AND TH{lvl}!=0")
        for building in cursor.fetchall():
            Main_base_buildings[lvl][category][building["name"]] = building[f"TH{lvl}"]
