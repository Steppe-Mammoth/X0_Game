from aiogram import types, F
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router
from bot.keyboards.callbacks.field_callback import Cell
from bot.states.users.game_states import BotGame
from game.android.vs_bot_game import XOBot


@private_router.callback_query(Cell.filter(F.used == False), state=BotGame.played)
async def press_vs_bot(call: types.CallbackQuery, callback_data: Cell, state: FSMContext):
    data = await state.get_data()
    game: XOBot = data.get('bot_game')

    unique_id_now = game.g_info.table.unique_id
    player_now = game.g_info.players.get_now_player()

    if callback_data.unique_id != unique_id_now:
        await call.answer('RETURN TO THE CURRENT GAME', show_alert=True, cache_time=-1)
        return

    if call.from_user.id != player_now.id:
        await call.answer('NOPE. NOT YOUR STEP', show_alert=True, cache_time=-1)
        return

    await game.next_game_step(index=callback_data.index_cell)
