from fastapi import Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from application.database import get_session
from application.schemas.user import UserGet, CreateUserDTO

from sqlalchemy.ext.asyncio import AsyncSession
from application.service.user import add_user, get_users, get_user_by_id


router = APIRouter()


@router.get('/users/', response_model=list[UserGet])
async def read_users(session: AsyncSession = Depends(get_session)):
    users_db = await get_users(session)

    users = [
        UserGet(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )
        for user in users_db
    ]

    return users


@router.post('/user/')
async def post_user(user: CreateUserDTO, session: AsyncSession = Depends(get_session)):
    user = add_user(session, user.username, user.email, user.password)

    try:
        await session.commit()
        return user
    except IntegrityError as e:
        await session.rollback()


@router.get('/user/{user_id}', response_model=UserGet)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await get_user_by_id(session, user_id)

    user = UserGet(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email,
        is_active=user_db.is_active
    )

    return user

# def delete_user(id: int, session: Session = Depends(get_session)):
#     user = session.query(user_models.User).get(id)
#
#     if user:
#         session.delete(user)
#         session.commit()
#     else:
#         raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')



# from typing import List
#
# from sqlalchemy.orm import Session
#
# from application.models import user as user_models
# from application.schemas import user as user_schemas
# from application.database import SessionLocal, Base, engine
#
# from fastapi import APIRouter, Depends, status, HTTPException
#
#
# Base.metadata.create_all(bind=engine)
#
# router = APIRouter()
#
#
# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()
#
#
#
#
#
# @router.post('/user', response_model=user_schemas.CreateUserDTO, status_code=status.HTTP_201_CREATED)
# def create_user(user: user_schemas.CreateUserDTO, session: Session = Depends(get_session)):
#     user_db = user_models.User(username=user.username, email=user.email, password=user.password)
#
#     session.add(user_db)
#     session.commit()
#     session.refresh(user_db)
#
#     return user_db
#
#
# @router.get('/user/{id}', response_model=user_schemas.User)
# def read_user(id: int, session: Session = Depends(get_session)):
#     user = session.query(user_models.User).get(id)
#
#     if not user:
#         raise HTTPException(status_code=404, detail=f'ser item with id {id} not found')
#
#     return user
#
#
# @router.put('/user/{id}', response_model=user_schemas.CreateUserDTO)
# def update_user(id: int, username: str, session: Session = Depends(get_session)):
#     user = session.query(user_models.User).get(id)
#
#     if user:
#         user.username = username
#         session.commit()
#     else:
#         raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')
#
#     return user
#
#
# @router.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(id: int, session: Session = Depends(get_session)):
#     user = session.query(user_models.User).get(id)
#
#     if user:
#         session.delete(user)
#         session.commit()
#     else:
#         raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')
#
#     return user
