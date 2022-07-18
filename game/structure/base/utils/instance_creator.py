from game.structure.base.data.dataclasses import GameParameters
from game.structure.others.technical import XOTechnic
from game.structure.players.data.dataclasses import PlayerInfo
from game.structure.base.game_info import GameInfo


class BaseCreator:

    @staticmethod
    def game_info_create(parameters: GameParameters) -> GameInfo:
        p1 = parameters.user_1
        p2 = parameters.user_2
        count_games = parameters.count_games
        symbols = XOTechnic.get_random_symbols()

        return GameInfo(player_1=PlayerInfo(user_id=p1.id, name=p1.full_name, symbol=symbols[0]),
                        player_2=PlayerInfo(user_id=p2.id, name=p2.full_name, symbol=symbols[1]),
                        count_games=count_games)
