from aiogram.types import User

from game.android.utils.android_person import create_name
from game.structure.others.technical import XOTechnic
from game.structure.players.data.dataclasses import PlayerInfo


def bot_create_players_object(user: User):
    p1 = user
    symbols = XOTechnic.get_random_symbols()

    return PlayerInfo(user_id=p1.id, name=p1.full_name, symbol=symbols[0]), \
           PlayerInfo(name=create_name(), symbol=symbols[1])
