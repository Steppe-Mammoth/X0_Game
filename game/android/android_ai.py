from typing import Optional

from game.structure.fields.utils.technical import TableBase


class BotAI:
    def __init__(self, p1_symbols, bot_symbols):
        self.win_combinations = TableBase.get_shuffle_combinations()
        self.p1_symbols: Optional[str] = p1_symbols
        self.bot_symbols: Optional[str] = bot_symbols

    def selected_cell(self, table: list) -> int:
        for row in self.win_combinations:
            row_table = [table[index] for index in row]
            # WIN

            if row_table.count(self.bot_symbols) == 2 and row_table.count(None) == 1:
                for index in row:
                    if table[index] is None:
                        return index

        for row in self.win_combinations:
            row_table = [table[index] for index in row]
            # помешать игроку с 2/3 набранных клеток в комбинации

            if row_table.count(self.p1_symbols) == 2 and row_table.count(None) == 1:
                for index in row:
                    if table[index] is None:
                        return index

        for row in self.win_combinations:
            row_table = [table[index] for index in row]
            # 1 есть и 2 пустых

            if row_table.count(self.bot_symbols) == 1 and row_table.count(None) == 2:
                for index in row:
                    if table[index] is None:
                        return index

        for row in self.win_combinations:
            row_table = [table[index] for index in row]
            # В выбранной комбинации все пустые ячейки -
            # вернет первый элемент так как комбинации в начале игры рандомизировались

            if row_table.count(None) == 3:
                return row[0]

        for row in self.win_combinations:
            for index in row:
                if table[index] is None:
                    return index
