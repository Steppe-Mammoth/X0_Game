from game.structure.players.data.dataclasses import PlayerInfo


def get_table_exit_game_text():
    text = f'''<i><b>* The game is over</b></i> *'''.upper()
    return text


def get_exit_game_text(player: PlayerInfo):
    text = f'<i><b>-🏃‍♂️ {player.name} capitulated 🏃‍♂️</b></i>'
    return text
