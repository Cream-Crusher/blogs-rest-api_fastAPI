from typing import List

from sqlalchemy import String, Column, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from application.database import Base
from application.models.associations import user_blogs_subscriptions, user_blogs_authors, users_post_likes


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    blogs_subscriptions: Mapped[List['Blog']] = relationship(
        secondary=user_blogs_subscriptions, back_populates='subscribed_users'
    )
    blogs_authors: Mapped[List['Blog']] = relationship(
        secondary=user_blogs_authors, back_populates='authors'
    )
    post_likes: Mapped[List['Post']] = relationship(
        secondary=users_post_likes, back_populates='likes'
    )
