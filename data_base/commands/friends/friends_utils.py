from operator import or_
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.commands.users.users_command import get_user
from data_base.structure.models_db import FriendsDB


async def _get_friends_id(session: AsyncSession, user_id: int):
    friends_id_list = []

    friends = await session.scalars(select(FriendsDB).where(or_(FriendsDB.user1_id == user_id,
                                                                FriendsDB.user2_id == user_id)))
    for user in friends:
        friend_id = user.user1_id if user.user2_id == user_id else user.user2_id
        friends_id_list.append(friend_id)

    return friends_id_list


async def _get_friends_user_object(session: AsyncSession, friends_id_list: Iterable):
    friends_user_objects = []
    for user_id in friends_id_list:
        friends_user_objects.append(await get_user(session, user_id=user_id))

    return tuple(friends_user_objects)