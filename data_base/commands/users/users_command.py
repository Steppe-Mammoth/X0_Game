from datetime import datetime

from aiogram.types import User
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from data_base.structure.models_db import UserDB


async def add_user(session: AsyncSession, user: User):
    user_db = UserDB()
    user_db.user_id = user.id
    user_db.username = user.username
    user_db.full_name = user.full_name
    user_db.created_on = datetime.utcnow()

    session.add(user_db)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int) -> UserDB | None:
    user = await session.scalar(select(UserDB).where(UserDB.user_id == user_id))
    return user


async def delete_user(session: AsyncSession, user_id):
    await session.execute(delete(UserDB).where(UserDB.user_id == user_id))
    await session.commit()
