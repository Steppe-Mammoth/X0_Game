from aiogram.types import User
from game.android.vs_bot_game import XOBot
from game.structure.base.data.dataclasses import GameParameters
from game.users.vs_user_game import XOUsers


class XO:
    @staticmethod
    def game_vs_user(parameters: GameParameters):
        return XOUsers(parameters)

    @staticmethod
    def game_vs_android(user: User):
        return XOBot(user=user)
