from aiogram.dispatcher.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    navigate = State()
    send_contact = State()
