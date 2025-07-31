If there is a Clash of Clans update I haven't added yet, please do a push request with the following changes:

### New TH/BH
* `data/data_source/clash_of_clans.sqlite`: Add a column in the database for the new TH/BH and fill in values
* `data/data_source/useful.json`: Change the `max_th/bh_lvl` value

### New buildings
* `data/data_source/clash_of_clans.db`: Add a line in the database for the new building and fill in values

### New troops
* `bot/emojis.py`: Add the new troop in the `emoji_to_name` variable
