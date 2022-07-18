import copy
import random


class TableBase:
    __table = [None] * 9
    __win_combinations = [[0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [6, 4, 2]]

    @classmethod
    def get_clear_table(cls) -> list:
        return cls.__table.copy()

    @classmethod
    def get_win_combinations(cls):
        return cls.__win_combinations.copy()

    @classmethod
    def get_shuffle_combinations(cls):
        combinations = copy.deepcopy(cls.__win_combinations)
        random.shuffle(combinations)
        [random.shuffle(row) for row in combinations]
        return combinations
