# from fastapi import FastAPI
# from application.database import engine
# from application.models.user import Base
# from application.routes.user import router
#
# app = FastAPI()
#
# # Инициализация базы данных
# Base.metadata.create_all(bind=engine)
#
# app.include_router(router)


from application.routes.user import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router)