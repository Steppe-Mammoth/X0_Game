import datetime
from typing import Optional

from aiogram import Bot, types

from app import logger, BotParam
from bot.keyboards.invite.invaite_keyboard import get_confirm_invite_keyboard
from text.menu_text.invited.invited_menu import InviteText


class InviteMessenger:
    def __init__(self, bot: Bot):
        self._bot = bot

        self.msg_wait_accept_invite: Optional[types.Message] = None
        """Сообщение об отправки приглашения и ожидания ответа"""
        self.msg_send_invite: Optional[types.Message] = None
        """Сообщение о приглашения в игру"""
        self.invite_time_sender: Optional[datetime.datetime] = None

    async def send_invitation_notification(self, p1: types.User, p2: types.User, rounds: int, invite_link: str):
        # Уведомления второго игрока о приглашении и отправка ему в колбеке уникальной ссылки в фсм дате
        text_send = InviteText.notification_invitation(name=p1.full_name, count_rounds=rounds)
        keyboard = get_confirm_invite_keyboard(invite_link=invite_link)

        msg = await self._bot.send_message(chat_id=p2.id, text=text_send, reply_markup=keyboard)

        self.msg_send_invite = msg
        self.invite_time_sender = datetime.datetime.utcnow()

        logger.info('_send_invitation_notification - DONE'.upper())

    async def notify_me_about_sending_invitation(self, p1: types.User):
        # Уведомить отправителя об отправке приглашения
        text_wait = InviteText.sender_invitation()
        msg_wait_invite = await self._bot.send_message(chat_id=p1.id, text=text_wait, disable_notification=True)
        self.msg_wait_accept_invite = msg_wait_invite

        logger.info('_notify_me_about_sending_invitation - DONE'.upper())

    async def delete_notify_about_sending_invitation(self):
        msg = self.msg_wait_accept_invite

        try:
            await BotParam.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        except Exception as e:
            logger.warning(e)

    async def auto_cancel_invite(self):
        # автоматически вызывается по истечению времени ожидания, убирает клавиатуру принятия приглашения получателю
        await self._bot.edit_message_reply_markup(chat_id=self.msg_send_invite.chat.id,
                                                  message_id=self.msg_send_invite.message_id, reply_markup=None)

        logger.info('_auto_cancel_invite (keyboard del) - DONE'.upper())

    async def notify_me_time_out(self, p1: types.User, p2: types.User):
        # автоматически вызывается по истечению времени ожидания, уведомляет пригласителя о истечении времени отклика
        await self.delete_notify_about_sending_invitation()
        await self._bot.send_message(chat_id=p1.id, text=f'<b>TIME OUT</b>\nINVITE FOR {p2.full_name.upper()} CANCEL')

        logger.info('_notify_me_time_out - DONE'.upper())

    async def notify_me_cancel_invite(self, p1: types.User, p2: types.User):
        # уведомляет пригласителя об отмене его приглашения
        await self.delete_notify_about_sending_invitation()

        text = InviteText.about_canceling_invitation(name=p2.full_name)
        await self._bot.send_message(chat_id=p1.id, text=text)

        logger.info('_notify_me_cancel_invite - DONE'.upper())