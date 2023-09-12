from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import relationship

from application.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    title = Column(String(50), index=True)
    body = Column(String),
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    views = Column(Integer, default=0)
