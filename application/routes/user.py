from typing import List

from sqlalchemy.orm import Session

from application.models import user as user_models
from application.schemas import user as user_schemas
from application.database import SessionLocal, Base, engine

from fastapi import APIRouter, Depends, status, HTTPException


Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.get('/users', response_model=List[user_schemas.User])
def read_users(session: Session = Depends(get_session)):
    user_list = session.query(user_models.User).all()

    return user_list


@router.post('/user', response_model=user_schemas.CreateUserDTO, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schemas.CreateUserDTO, session: Session = Depends(get_session)):
    user_db = user_models.User(username=user.username, email=user.email, password=user.password)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.get('/user/{id}', response_model=user_schemas.User)
def read_user(id: int, session: Session = Depends(get_session)):
    user = session.query(user_models.User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail=f'ser item with id {id} not found')

    return user


@router.put('/user/{id}', response_model=user_schemas.CreateUserDTO)
def update_user(id: int, username: str, session: Session = Depends(get_session)):
    user = session.query(user_models.User).get(id)

    if user:
        user.username = username
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')

    return user
#
#
@router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_session)):
    user = session.query(user_models.User).get(id)

    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')

    return user