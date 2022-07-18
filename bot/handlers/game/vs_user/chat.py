import html

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router
from bot.states.users.game_states import PlayerGame
from game.users.vs_user_game import XOUsers
from app import logger


@private_router.message_handler(state=PlayerGame.played)
async def chat(message: types.Message, state: FSMContext):
    msg_text = message.text

    try:
        msg_text = html.escape(message.text)
    except Exception as e:
        logger.warining(f'{e} ||\n --{message.text} -> not replace html')

    data = await state.get_data()
    game: XOUsers = data.get('game_player')

    await game.chat_refresh(text=msg_text)
    await message.delete()
