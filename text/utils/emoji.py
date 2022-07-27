import random
from copy import copy


class GetEmoji:
    _crayfish = '🦑', '🦐', '🦞', '🦀', '🦂', '🦅'

    _duel_fight = '🤼‍♂', '🤼', '🤼‍♀'

    _sport = '🤽🏻‍♂', '🚴', '🚴‍', '🚴🏻‍♂', '🏄‍♀', '🏄🏾', '🏄🏿‍', '🏊🏻‍', '⛹🏿‍', '⛹🏿', '⛹🏿‍', '🤺', '🏌🏻‍', '🏌️', '🏌️', '🏋️‍', \
             '🏋️', '🏋🏼‍', '🏂', '🤽🏻‍', '🚴', '🚴‍'

    _smile = '🤟', '🤩', '🥸', '😎', '🧐', '🤠', '🤒', '🤕', '👻', '🤖', '👹', '🤔', '🥳', '🤪', '🤨', '👀'

    _people = '🧝🏾‍♀️', '🧝‍♂️', '🧛🏿‍♂️', '🧑‍🚀', '👩🏼‍💼', '👨🏾‍💼', '👨‍✈️', '👨🏻‍🔬', '👨🏻‍🔧', '👨🏻‍🎨', '🎅🏿', '👰🏻‍♂️',\
              '👰🏼', '👨🏻‍🍳', '👮🏿', '👮🏻‍♂️', '👮‍♀️', '👳🏽‍♂️', '👲', ' 🧔‍♀️', '👷‍♂️', '👩🏽‍🌾', '🧑🏻‍🌾', '👨‍🌾', '👩‍🏭',\
              '👺', '👹'

    _silent = '🗣', '👤', '👥', '🫂'

    _robot = '📼', '⌚', '💻', '🖨', '🕹', '🗜', '💾', '📼', '📟', '☎', '📺', '📻', '⏰', '⏲', '🤖', '📽', '📠'

    _guns = '⛏', '🪚', '🗡', '🔪', '🪓', '💣', '🧨', '🔨', '🪛'

    _envelope = '📪', '📫', '📬', '📭', '📧', '✉', '📨', '📮'

    _symbols_chat = '🔺', '🔻', '🔸', '🔹', '▫️'

    _replay_symbols = '🔀', '🔁', '🔂', '🔄', '🔃', '↪', '↩'

    @classmethod
    def crayfish(cls, count):
        return cls._r_choices(emojis=cls._crayfish, count=count)

    @classmethod
    def duel_fight(cls, count):
        return cls._r_choices(emojis=cls._duel_fight, count=count)

    @classmethod
    def sport(cls, count):
        return cls._r_choices(emojis=cls._sport, count=count)

    @classmethod
    def smile(cls, count):
        return cls._r_choices(emojis=cls._smile, count=count)

    @classmethod
    def replay_symbols(cls, count):
        return cls._r_choices(emojis=cls._replay_symbols, count=count)

    @classmethod
    def people(cls, count: int = None, generator: bool = False):
        emojis = cls._people

        if count:
            return cls._r_choices(emojis=cls._people, count=count)
        if generator:
            return cls._r_generator(emojis)

    @classmethod
    def silent(cls, count):
        return cls._r_choices(emojis=cls._silent, count=count)

    @classmethod
    def robot(cls, count):
        return cls._r_choices(emojis=cls._robot, count=count)

    @classmethod
    def guns(cls, count):
        return cls._r_choices(emojis=cls._guns, count=count)

    @classmethod
    def symbols_chat_generator(cls):
        return cls._r_generator(emojis=cls._symbols_chat)

    @classmethod
    def envelope(cls, count):
        return cls._r_choices(emojis=cls._envelope, count=count)

    @classmethod
    def _r_generator(cls, emojis: tuple):
        emojis = cls._r_copy_shuffle(emojis)
        while True:
            for emoji in emojis:
                yield emoji

    @classmethod
    def _r_choices(cls, emojis: tuple, count):
        emojis = cls._r_copy_shuffle(emojis)
        return tuple(random.choices(emojis, k=count))

    @staticmethod
    def _r_copy_shuffle(emojis: tuple):
        copy_emojis = list(copy(emojis))
        random.shuffle(copy_emojis)
        return copy_emojis
