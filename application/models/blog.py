from typing import List

from sqlalchemy import String, Column, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from application.database import Base
from application.models.associations import user_blogs_subscriptions, user_blogs_authors


class Blog(Base):
    __tablename__ = 'blogs'

    id: Mapped[int] = mapped_column(primary_key=True)

    title = Column(String(50), index=True)
    description = Column(String(150), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    subscribed_users: Mapped[List['User']] = relationship(
        secondary=user_blogs_subscriptions, back_populates='blogs_subscriptions'
    )
    authors: Mapped[List['User']] = relationship(
        secondary=user_blogs_authors, back_populates='blogs_authors'
    )

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User')

    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    posts = relationship('Post')
