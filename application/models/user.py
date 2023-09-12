from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, mapped_column

from application.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    user_id = mapped_column(ForeignKey('users.id'))
    subscriptions = relationship('Blog', back_populates="user")
