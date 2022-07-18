import random


def create_name():
    first_names = ('THOUGHTFUL', "NUTS", 'BIG', 'SEXY ', 'MR.', 'GYPSY', 'HOLY', 'OLD', 'CUNNING', 'MINER',)
    last_names = ('GRANDMASTER', "HACKER", 'CHANG', 'BORIS JOHNSON', 'PRESIDENT', "ROBOCOP", "CALCULANT", "RANDOMIZER",
                  'INTEL PENTIUM', 'DANCER', 'STATHEM', 'ALGORITHM', 'HERODOTUS', 'TESLA', 'NEO', 'MORPHEUS', 'SELLER',
                  'CHAMPION', 'CHESS PLAYER', 'VIRUS', 'FOUNDER OF NETWORK NAZIS')

    full_name = random.choice(first_names) + ' ' + random.choice(last_names)
    return full_name
