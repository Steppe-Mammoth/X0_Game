from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router
from bot.states.users.game_states import PlayerGame
from game.users.vs_user_game import XOUsers

from bot.utils.user_utils.user_fsm import set_user_fsm


@private_router.message_handler(commands='exit', state=PlayerGame.played)
async def exit_game(message: types.Message, state: FSMContext):
    data = await state.get_data()
    game: XOUsers = data.get('game_player')

    player = game.g_info.players.get_player(message.from_user.id)
    players = game.g_info.players.get_players()

    await game.exit_game(exit_player=player)

    for player in players:
        await set_user_fsm(user_id=player.id, chat_id=player.id, state=state, clear=True)
