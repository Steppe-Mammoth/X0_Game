from typing import NamedTuple, Optional
from game.structure.message.data.dataclasses import MessageInfo, MessageVoteInfo


class PlayerInfo:
    def __init__(self, name: str, symbol: str = None, user_id: int = None):
        self.id: Optional[int] = user_id
        self.name: str = name
        self.symbol: str = symbol
        self.emoji: str = self.get_emoji()
        self.count_winner: int = 0

        self.msg_table: Optional[MessageInfo] = None
        self.msg_stat: Optional[MessageInfo] = None
        self.msg_chat: Optional[MessageInfo] = None
        self.msg_vote: Optional[MessageVoteInfo] = None

    def add_winner(self):
        self.count_winner += 1

    def get_emoji(self):
        return '❎' if self.symbol == 'X' else '🅾️'


class WinnerLoser(NamedTuple):
    winner: PlayerInfo
    loser: PlayerInfo
