from fastapi import FastAPI
from application.database import engine
from application.models.user_model import Base
from application.routes.user_route import router

app = FastAPI()

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

app.include_router(router)
