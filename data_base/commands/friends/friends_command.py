from datetime import datetime
from operator import or_, and_

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.commands.friends.friends_utils import _get_friends_id, _get_friends_user_object
from data_base.structure.models_db import FriendsDB


async def add_friends(session: AsyncSession, user1_id: int, user2_id: int):
    friends = FriendsDB()
    friends.user1_id = user1_id
    friends.user2_id = user2_id
    friends.created_on = datetime.utcnow()

    session.add(friends)
    await session.commit()


async def get_friends(session: AsyncSession, user_id: int):
    friends_id = await _get_friends_id(session, user_id=user_id)
    friends_objects = await _get_friends_user_object(session, friends_id_list=friends_id)
    return friends_objects


async def check_friends(session: AsyncSession, user1_id: int, user2_id: int):
    return await session.scalar(
        select(FriendsDB).where(or_(and_(FriendsDB.user1_id == user1_id, FriendsDB.user2_id == user2_id),
                                    and_(FriendsDB.user1_id == user2_id, FriendsDB.user2_id == user1_id))))
