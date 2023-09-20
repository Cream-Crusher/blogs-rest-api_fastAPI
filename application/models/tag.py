from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column

from application.database import Base


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)

    tag_name = Column(String(20), unique=True)
