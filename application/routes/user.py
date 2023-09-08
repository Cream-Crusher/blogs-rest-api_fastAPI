from typing import List

from sqlalchemy.orm import Session

from application.models import user as user_models
from application.schemas import user as user_schemas
from application.database import SessionLocal, Base, engine

from fastapi import APIRouter, Depends, status


Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.get("/user", response_model=List[user_schemas.User])
def read_todo_list(session: Session = Depends(get_session)):
    user_list = session.query(user_models.User).all()

    return user_list


@router.post("/user", response_model=user_schemas.CreateUserDTO, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.CreateUserDTO, session: Session = Depends(get_session)):
    user_db = user_models.User(username=user.username, email=user.email, password=user.password)

    # add it to the session and commit it
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


# @router.get('user/{id}')
# def get_user(id: int):
#     return '#'

#
# @router.post('user/creted', status_code=status.HTTP_201_CREATED)
# def create_user(user: UserRequest):
#     return '#'
#
#
# @router.put('user/{id}')
# def update_user(id: int):
#     return '#'
#
#
# @router.delete("user/{id}")
# def delete_todo(id: int):
#     return '#'
#
#
