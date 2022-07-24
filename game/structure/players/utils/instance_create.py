from aiogram.types import User

from game.android.utils.android_person import create_name
from game.structure.others.technical import XOTechnic
from game.structure.players.data.dataclasses import PlayerInfo


def bot_create_players_object(user: User) -> tuple[PlayerInfo, PlayerInfo]:
    symbols = XOTechnic.get_random_symbols()

    player = PlayerInfo(user_id=user.id, name=user.full_name, symbol=symbols[0])
    bot = PlayerInfo(name=create_name(), symbol=symbols[1])

    return player, bot
