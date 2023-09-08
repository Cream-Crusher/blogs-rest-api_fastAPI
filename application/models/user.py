# from sqlalchemy import Column, Integer, String, Boolean
# from application.database import Base
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String)
#     is_active = Column(Boolean, default=True)

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from application.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    population = Column(Integer)
