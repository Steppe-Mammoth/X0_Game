from aiogram.dispatcher.fsm.state import StatesGroup, State


class PlayerGame(StatesGroup):
    played = State()
    vote = State()


class BotGame(StatesGroup):
    played = State()
