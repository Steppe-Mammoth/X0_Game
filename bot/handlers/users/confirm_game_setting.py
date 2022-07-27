from aiogram import types, F, Bot
from aiogram.dispatcher.fsm.context import FSMContext

from bot.states.users.menu_states import Menu
from bot.utils.inviter.invite_sender import Inviter
from bot.utils.inviter.utils.user_invite_check import check_access_for_invite
from text.menu_text.invited.invited_menu import InviteText

from text.menu_text.started_menu.menu_text import MenuText
from bot.handlers.routers import private_router

from bot.callbacks.setting_callback import SettingAccept
from bot.callbacks.user_callback import OpponentCB
from bot.keyboards.menu.confirm_setting_keyboard import get_confirm_setting_keyboard


@private_router.callback_query(OpponentCB.filter(F.count_rounds != 0), state=Menu.navigate)
async def confirm_setting(call: types.CallbackQuery, callback_data: OpponentCB, bot: Bot):
    count_rounds = callback_data.count_rounds
    opponent_id = callback_data.user_id
    opponent = (await bot.get_chat_member(chat_id=opponent_id, user_id=opponent_id)).user

    text = MenuText.show_game_description(opponent.full_name, count_rounds=count_rounds)
    await call.message.edit_text(text=text, reply_markup=get_confirm_setting_keyboard(user_id=opponent.id,
                                                                                      count_rounds=count_rounds))


@private_router.callback_query(SettingAccept.filter(), state=Menu.navigate)
async def confirm_game_setting(call: types.CallbackQuery, callback_data: SettingAccept, state: FSMContext, bot: Bot):
    # Потвердить выбраные парметры и отправить приглашение
    user_1 = call.from_user
    user_2_id = callback_data.opponent_id
    user_2 = (await bot.get_chat_member(user_2_id, user_2_id)).user

    pre_inviter: Inviter = (await state.get_data()).get('inviter')

    if pre_inviter and pre_inviter.access is None:
        seconds = pre_inviter.get_remaining_active_time()
        text = InviteText.watch_wait_time(seconds)
        await call.answer(text=text, show_alert=True)
        return

    if await check_access_for_invite(user_id=user_2.id, state=state, bot=bot) is False:
        await call.answer('WAIT\nTHIS PLAYER NOW PLAYING GAME!', show_alert=True)
        return

    inviter = Inviter(bot=bot, user_1=user_1, user_2=user_2, count_rounds=callback_data.count_rounds)
    await call.message.delete_reply_markup()

    await inviter.send_invite(state=state)
