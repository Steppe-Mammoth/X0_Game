from aiogram.types import User
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, BigInteger, DateTime
from datetime import datetime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'))
    user_id = Column(BigInteger, unique=True, primary_key=True)
    username = Column(String(70))
    full_name = Column(String(70), nullable=False)
    created_on = Column(DateTime)

    def __init__(self, user: User):
        self.user_id = user.id
        self.username = user.username
        self.full_name = user.full_name
        self.created_on = datetime.utcnow()


class FriendsDB(Base):
    __tablename__ = 'friends'

    id = Column(Integer, Sequence('friends_id_seq'), primary_key=True)
    user1_id = Column(BigInteger, ForeignKey("users.user_id"))
    user2_id = Column(BigInteger, ForeignKey("users.user_id"))

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
