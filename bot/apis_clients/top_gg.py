import topgg

from data.config import Config
from data.secure_folder import Login
from data.useful import Ids


if Config["top_gg"]:
    Dbl_client = topgg.DBLClient(token=Login["top_gg"]["token"], default_bot_id=Ids["Bot"])
