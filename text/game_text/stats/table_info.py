from typing import Sequence

from game.structure.players.data.dataclasses import PlayerInfo
from text.utils.emoji import GetEmoji


def get_table_info_text(players: Sequence[PlayerInfo], count_selected_games: int, count_games_played: int):
    p1 = players[0]
    p2 = players[1]

    p1_name = p1.name.split()[0]
    p2_name = p2.name.split()[0]

    people = GetEmoji.people(2)

    text = f'''⠀<i><b>{people[0]} {p1_name.upper()}</b> vs <b>{p2_name.upper()} {people[1]}</b></i>

    <u>{'*' * 30}</u>
    <i><b>VICTORY COUNTER:</b>
    {p1.name}: {p1.count_winner} / {count_selected_games}
    {p2.name}: {p2.count_winner} / {count_selected_games}</i>
    <u>{'*' * 30}</u>
    <b>GAMES PLAYED: {count_games_played}</b>
    '''
    return text


def get_first_player_step_text(player_now: PlayerInfo):
    player_text = get_player_text(player_now)
    text = player_text + '\nyour first turn'.upper()
    return text


def get_now_player_step_text(player_now: PlayerInfo):
    player_text = get_player_text(player_now)
    text = player_text + '\nyour turn now'.upper()
    return text


def get_player_text(player_now: PlayerInfo):
    text = f'<b>{player_now.name}</b> {player_now.emoji}'
    return text


def get_present_players(players: Sequence[PlayerInfo]):
    p1_name = players[0].name.split()[0].upper()
    bot_name = players[1].name

    people_emoji = GetEmoji.people(count=1)
    bot_emoji = GetEmoji.robot(count=1)

    text = f"<i><b>{bot_name} {bot_emoji[0]} vs {people_emoji[0]} {p1_name}</b></i>"
    return text
