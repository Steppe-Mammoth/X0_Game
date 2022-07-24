from game.structure.players.data.dataclasses import PlayerInfo


def get_game_table_capitulated_text():
    text = '''<i><b>* The game is over</b></i> *'''.upper()
    return text


def get_game_capitulated_text(player: PlayerInfo):
    text = f'<i><b>-🏃‍♂️ {player.name} capitulated 🏃‍♂️</b></i>'
    return text
