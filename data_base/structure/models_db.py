from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, BigInteger, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'))
    user_id = Column(BigInteger, unique=True, primary_key=True)
    username = Column(String(70))
    full_name = Column(String(70), nullable=False)
    created_on = Column(DateTime)


class FriendsDB(Base):
    __tablename__ = 'friends'

    id = Column(Integer, Sequence('friends_id_seq'), primary_key=True)
    user1_id = Column(BigInteger, ForeignKey("users.user_id", ondelete='CASCADE'))
    user2_id = Column(BigInteger, ForeignKey("users.user_id", ondelete='CASCADE'))
    created_on = Column(DateTime)
