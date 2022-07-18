from typing import Sequence

from game.structure.players.data.dataclasses import PlayerInfo
from text.utils.lines import get_symbols_line_text


def get_started_text_for_retry_game():
    line = get_symbols_line_text()
    text = '<b>CHOICE:</b> <i><u>RETRY</u> OR <u>EXIT</u> GAME</i>'.upper()

    end_text = line + '\n' + text
    return end_text


def get_retry_game_vote_text(players: Sequence[PlayerInfo]) -> str:
    text = f'<b><u>VOTE FOR PLAY AGAIN</u>:</b>\n'
    for user in players:
        choice = user.msg_vote.choice
        choice_symbol = '👍' if choice is True else '👎' if choice is False else ''

        user_vote = f'\n<b>{user.name}</b>: {choice_symbol}'
        text += user_vote

    return text
