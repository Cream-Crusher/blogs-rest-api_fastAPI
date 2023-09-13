from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from application.models.blog import Blog  # not del | used

from application.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    subscriptions = relationship('Blog', back_populates='user', lazy='selectin')
