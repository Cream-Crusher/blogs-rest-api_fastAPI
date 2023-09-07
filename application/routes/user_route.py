from fastapi import APIRouter, status
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

router = APIRouter()

@router.get("/")
def root():
    return "todoooq"

