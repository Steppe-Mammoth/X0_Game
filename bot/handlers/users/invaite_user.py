from aiogram import types, F
from aiogram.dispatcher.fsm.context import FSMContext

from bot.handlers.routers import private_router

from bot.keyboards.callbacks.invite_callback import Invite
from bot.states.users.game_states import BotGame

from bot.states.users.menu_states import Menu
from bot.utils.inviter.invite_sender import Inviter

from bot.utils.inviter.utils.user_invite_check import check_access_for_invite


@private_router.callback_query(Invite.filter(F.choice == True), state=(Menu.navigate, BotGame.played, None))
async def accept_invitation(call: types.CallbackQuery, callback_data: Invite, state: FSMContext):
    # приянть приглашение
    invite_link = callback_data.invite_link
    invite: Inviter = (await state.get_data()).get(invite_link)

    if await check_access_for_invite(user_id=invite.parameters.user_1.id, state=state) is False:
        await call.answer('WAIT\nTHIS PLAYER NOW PLAYING GAME', show_alert=True)
        return

    await call.message.delete_reply_markup()
    await invite.press_accept_invite(state=state)


@private_router.callback_query(Invite.filter(F.choice == False), state=(Menu.navigate, BotGame.played, None))
async def cancel_invitation(call: types.CallbackQuery, callback_data: Invite, state: FSMContext):
    # отклонить приглашение

    invite_link = callback_data.invite_link
    invite: Inviter = (await state.get_data()).get(invite_link)

    await call.message.delete_reply_markup()

    await invite.press_cancel_invite(state=state)
    await call.message.answer(text='<b><i>Invitation canceled</i></b>'.upper())
