from sqlalchemy import Column, String

from application.database import Base


class tag(Base):
    __tablename__ = 'tags'

    id = Column(String, autoincrement=True, primary_key=True, index=True)
    tag_name = Column(String(20), unique=True)
