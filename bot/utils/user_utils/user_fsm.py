from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State
from aiogram.dispatcher.fsm.storage.base import StorageKey

from app import BotParam


async def set_user_fsm(user_id: int, chat_id: int, state: FSMContext,
                       set_data: dict = None,
                       update_data: dict = None,
                       user_state: State = None,
                       clear: bool = False):

    key = StorageKey(bot_id=BotParam.bot.id, chat_id=chat_id, user_id=user_id)

    if set_data:
        await state.storage.set_data(bot=BotParam.bot, key=key, data=set_data)
    if update_data:
        await state.storage.update_data(bot=BotParam.bot, key=key, data=update_data)
    if user_state:
        await state.storage.set_state(bot=BotParam.bot, key=key, state=user_state)
    if clear:
        await state.storage.set_data(bot=BotParam.bot, key=key, data={})
        await state.storage.set_state(bot=BotParam.bot, key=key, state=None)


async def get_user_state(user_id: int, chat_id: int, state: FSMContext):
    key = StorageKey(bot_id=BotParam.bot.id,
                     chat_id=chat_id,
                     user_id=user_id)

    return await state.storage.get_state(bot=BotParam.bot, key=key)


async def get_user_data(user_id: int, chat_id: int, state: FSMContext):
    key = StorageKey(bot_id=BotParam.bot.id,
                     chat_id=chat_id,
                     user_id=user_id)

    return await state.storage.get_data(bot=BotParam.bot, key=key)