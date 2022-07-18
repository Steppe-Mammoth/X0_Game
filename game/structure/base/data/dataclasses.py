from dataclasses import dataclass
from typing import Optional

from aiogram.types import User


@dataclass
class GameStats:
    count_selected_games: Optional[int] = None
    count_games_played: int = 0
    count_peace: int = 0

    def add_played_game(self, peace: bool = False):
        self.count_games_played += 1
        if peace:
            self.count_peace += 1


@dataclass
class GameParameters:
    user_1: User
    """sender"""

    user_2: User
    """recipient"""

    count_games: int

    def edit_count_games(self, count: int):
        self.count_games = count

