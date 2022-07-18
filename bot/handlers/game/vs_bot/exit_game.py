from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router
from bot.states.users.game_states import BotGame
from game.android.vs_bot_game import XOBot


@private_router.message_handler(commands='exit', state=BotGame.played)
async def exit_game(message: types.Message, state: FSMContext):
    data = await state.get_data()
    game: XOBot = data.get('bot_game')

    player = game.g_info.players.get_player(message.from_user.id)

    await game.exit_game(exit_player=player)
    await state.clear()
