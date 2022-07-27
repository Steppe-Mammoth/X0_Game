from aiogram import types, F
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router
from bot.callbacks.field_callback import Cell
from bot.states.users.game_states import PlayerGame

from game.users.vs_user_game import XOUsers


@private_router.callback_query(Cell.filter(F.used == False), state=PlayerGame.played)
async def press_vs_player(call: types.CallbackQuery, callback_data: Cell, state: FSMContext):
    data = await state.get_data()
    game: XOUsers = data.get('game_player')

    unique_id_now = game.g_info.table.unique_id
    player_now = game.g_info.players.get_now_player()

    if callback_data.unique_id != unique_id_now:
        await call.answer('RETURN TO THE CURRENT GAME', show_alert=True, cache_time=-1)
        return

    if call.from_user.id != player_now.id:
        await call.answer('NOPE. NOT YOUR STEP', show_alert=True, cache_time=-1)
        return

    await game.next_game_step(index=callback_data.index_cell)
