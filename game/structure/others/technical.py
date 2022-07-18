import random
import string


class XOTechnic:
    symbols = string.ascii_letters + string.digits
    len_unique_id = 4

    @staticmethod
    def get_random_symbols() -> tuple[str, ...]:
        symbols = ['X', '0'].copy()
        random.shuffle(symbols)
        return tuple(symbols)

    @classmethod
    def get_unique_id(cls):
        unique_id = ''

        for symbol in range(cls.len_unique_id):
            unique_id += random.choice(cls.symbols)
        return unique_id
