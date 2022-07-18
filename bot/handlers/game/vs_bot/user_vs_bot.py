from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router
from bot.states.users.game_states import BotGame
from game.app import XO


@private_router.callback_query(text='user_vs_bot')
async def user_vs_bot_mode(call: CallbackQuery, state: FSMContext, bot: Bot):
    game = XO.game_vs_android(user=call.from_user)

    await state.update_data(bot_game=game)
    await state.set_state(BotGame.played)

    await call.message.delete_reply_markup()
    await game.new_game_initialization(bot)
