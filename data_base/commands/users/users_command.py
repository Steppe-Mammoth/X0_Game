from aiogram.types import User
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.structure.models_db import UserDB, FriendsDB


async def add_friends(session: AsyncSession, my_user_id: int, friend_user_id: int):
    friends = FriendsDB(user1_id=my_user_id, user2_id=friend_user_id)

    session.add(friends)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int) -> UserDB | None:
    user = await session.scalar(select(UserDB).where(UserDB.user_id == user_id))
    return user


async def add_user(session: AsyncSession, user: User):
    user_db = UserDB(user=user)
    session.add(user_db)
    await session.commit()


async def delete_user(session: AsyncSession, user_id):
    await session.execute(delete(UserDB).where(UserDB.user_id == user_id))
    await session.commit()
