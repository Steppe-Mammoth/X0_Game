from aiogram import F, types

from bot.handlers.routers import private_router
from bot.callbacks.field_callback import Cell


@private_router.callback_query(Cell.filter(F.finish == True), state='*')
async def notify_finish_game(call: types.CallbackQuery):
    await call.answer('THIS GAME IS FINISHED', show_alert=True, cache_time=-1)


@private_router.callback_query(Cell.filter(F.used == True), state='*')
async def notify_used_cell(call: types.CallbackQuery):
    await call.answer('THIS CELL USED', show_alert=True, cache_time=-1)
