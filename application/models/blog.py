from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from application.database import Base


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    title = Column(String(50), index=True)
    description = Column(String(150), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="subscriptions")
