from sqlalchemy import Column, String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from application.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)

    body = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User')

    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    post = relationship('Post')
