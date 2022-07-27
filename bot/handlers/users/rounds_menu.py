from aiogram import F, types

from bot.handlers.routers import private_router
from bot.callbacks.user_callback import OpponentCB
from bot.keyboards.menu.select_rounds_keyboard import get_count_rounds_keyboard
from bot.states.users.menu_states import Menu
from text.menu_text.started_menu.menu_text import MenuText


@private_router.callback_query(OpponentCB.filter(F.count_rounds == 0), state=Menu.navigate)
async def select_count_rounds(call: types.CallbackQuery, callback_data: OpponentCB):
    opponent_id = callback_data.user_id

    text = MenuText.select_rounds()
    await call.message.edit_text(text=text, reply_markup=get_count_rounds_keyboard(user_id=opponent_id))
