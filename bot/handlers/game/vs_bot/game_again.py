from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import Bot

from bot.handlers.routers import private_router
from bot.states.users.game_states import BotGame
from game.android.vs_bot_game import XOBot
from logger import logger


@private_router.callback_query(text='retry_game_bot', state=BotGame.played)
async def bot_game_again(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.delete_reply_markup()

    data = await state.get_data()
    game: XOBot = data.get('bot_game')

    await game.new_game_initialization(bot)
    logger.info('RESTART BOT GAME')


@private_router.callback_query(text='exit_in_menu', state=BotGame.played)
async def bot_exit_game(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.clear()

    logger.info('EXIT TO MENU')
