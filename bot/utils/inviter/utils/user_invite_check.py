import datetime
from bot.utils.user_utils.user_fsm import get_user_state


async def check_access_for_invite(user_id, state, bot):
    """Проверяет не находится ли юзер в игровых состояниях"""
    state_user = await get_user_state(user_id=user_id, chat_id=user_id, state=state, bot=bot)

    if state_user in ('PlayerGame:played', 'PlayerGame:vote'):
        return False
    else:
        return True


def check_time_for_invite(message_time: datetime.datetime, check_seconds: int):
    t_delta = datetime.timedelta(seconds=check_seconds)

    if (message_time + t_delta) > datetime.datetime.utcnow():
        return True
    else:
        return False
