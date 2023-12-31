from typing import List

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from application.database import Base
from application.models.associations import users_post_likes


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)

    title = Column(String(50), index=True)
    body = Column(String)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    views = Column(Integer, default=0)

    likes: Mapped[List['User']] = relationship(
        secondary=users_post_likes, back_populates='post_likes'
    )
    tags: Mapped[List['Tag']] = relationship(
        secondary='association_table_tags'
    )

    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User')

    blog_id = Column(Integer, ForeignKey('blogs.id'))
    blog = relationship('Blog', back_populates='posts')
