from sqlalchemy import Column, String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship

from application.database import Base


class comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    body = Column(String)
    created_at = Column(DateTime, server_default=func.now())
