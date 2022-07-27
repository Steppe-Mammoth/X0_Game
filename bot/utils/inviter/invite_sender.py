import datetime
from aiogram import types, Bot
from asyncio import sleep
from typing import Optional

from logger import logger
from bot.utils.inviter.utils.invite_messenger import InviteMessenger

from game.app import XO
from game.users.vs_user_game import XOUsers
from game.structure.base.data.dataclasses import GameParameters

from bot.states.users.game_states import PlayerGame
from bot.utils.user_utils.user_fsm import set_user_fsm, get_user_data


class Inviter:
    _wait_time = 45
    """Время для на принятие приглашения"""

    def __init__(self, bot: Bot, user_1: types.User, user_2: types.User, count_rounds: int):
        self._bot = bot
        self.messenger: InviteMessenger = InviteMessenger(bot=bot)
        self.parameters: GameParameters = GameParameters(user_1=user_1, user_2=user_2, count_games=count_rounds)
        self.link: str = self._get_invite_link()

        self.access: Optional[bool] = None

    async def send_invite(self, state):
        p1 = self.parameters.user_1
        p2 = self.parameters.user_2
        rounds = self.parameters.count_games

        await self._set_fsm_invite_data(p1=p1, p2=p2, state=state)
        await self.messenger.send_invitation_notification(p1=p1, p2=p2, rounds=rounds, invite_link=self.link)
        await self.messenger.notify_me_about_sending_invitation(p1=p1)

        await sleep(self._wait_time)

        if self.access is None:

            self.access = False
            await self.messenger.auto_cancel_invite()
            await self.messenger.notify_me_time_out(p1=p1, p2=p2)
            await self._set_old_fsm(p1=p1, p2=p2, state=state)

            logger.info('auto timer del invite - done'.upper())

    def get_remaining_active_time(self) -> int:
        # показывает оставившейся время ожидания ответа на приглашения
        time_now = datetime.datetime.utcnow()
        time_sender = self.messenger.invite_time_sender
        time_wait = datetime.timedelta(seconds=self._wait_time)

        time = time_wait - (time_now - time_sender)
        return time.seconds

    async def _set_fsm_invite_data(self, p1: types.User, p2: types.User, state):
        # для отправителя устанавливается общая стейт_дата "инвайт", для того что бы повторно нельзя было слать
        # пригласительных
        # для получателя будет формироватся особый линк для реагирования к примеру на два одновременных запроса на игру

        await set_user_fsm(user_id=p1.id, chat_id=p1.id, state=state, bot=self._bot, update_data={"inviter": self})
        await set_user_fsm(user_id=p2.id, chat_id=p2.id, state=state, bot=self._bot, update_data={self.link: self})

        logger.info('_set_fsm_invite_data - DONE'.upper())

    async def press_cancel_invite(self, state):
        p1 = self.parameters.user_1
        p2 = self.parameters.user_2
        self._set_access(False)

        await self.messenger.notify_me_cancel_invite(p1=p1, p2=p2)
        await self._set_old_fsm(p1=p1, p2=p2, state=state)

        logger.info('**press_cancel_invite - DONE'.upper())

    async def press_accept_invite(self, state):
        """Create and set game instance"""
        self._set_access(True)
        await self._create_game(state=state)

        logger.info('**press_accept_invite - DONE'.upper())

    async def _set_old_fsm(self, p1: types.User, p2: types.User, state):
        """Удаляет для каждого пользователя его пригласительные ссылки"""
        invite_link = self._get_invite_link()

        p1_data = await get_user_data(p1.id, p1.id, state=state, bot=self._bot)
        p1_data.pop('inviter')
        await set_user_fsm(user_id=p1.id, chat_id=p1.id, state=state, bot=self._bot, set_data=p1_data)

        p2_data = await get_user_data(p2.id, p2.id, state=state, bot=self._bot)
        p2_data.pop(invite_link)
        await set_user_fsm(user_id=p2.id, chat_id=p2.id, state=state, bot=self._bot, set_data=p2_data)

        logger.info('_set_old_fsm_invite_data - DONE'.upper())

    async def _create_game(self, state):
        game = XO.game_vs_user(parameters=self.parameters)

        await self.messenger.delete_notify_about_sending_invitation()
        await game.new_game_initialization(bot=self._bot)

        await self._set_game_fsm(state=state, game=game)
        await game.start_new_party()

        logger.info('create_game - DONE'.upper())

    async def _set_game_fsm(self, state, game: XOUsers):
        p1 = self.parameters.user_1
        p2 = self.parameters.user_2

        for player in p1, p2:
            await set_user_fsm(user_id=player.id, chat_id=player.id,
                               state=state, bot=self._bot,
                               set_data={"game_player": game}, user_state=PlayerGame.played)

        logger.info('set_game_fsm_state_data - DONE'.upper())

    def _set_access(self, choice: bool):
        self.access = choice

    def _get_invite_link(self):
        return f"{self.parameters.user_1.id}_{self.parameters.user_2.id}"

    def __del__(self):
        logger.warning(f'** {self.link} INVITED DELETE - DONE'.upper())
