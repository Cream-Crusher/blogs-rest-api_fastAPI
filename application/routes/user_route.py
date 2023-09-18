from fastapi import Depends, APIRouter, HTTPException

from application.database import get_session
from application.schemas.user import GetUserDTO, CreateUserDTO, DeleteUserDTO, UpdateUserDTO, GetUsersDTO
from application.services.user_service import get_and_create_user, get_users, get_user, get_and_update_user

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get('/users/', response_model=list[GetUsersDTO], tags=['Tag'])
async def read_users(session: AsyncSession = Depends(get_session)):
    users_db = await get_users(session)

    if not users_db:
        raise HTTPException(status_code=400, detail=('Users not found'))

    users_db = [
        GetUsersDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )
        for user in users_db
    ]

    return users_db


@router.get('/user/{user_id}', response_model=GetUserDTO, tags=['Tag'])
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await get_user(session, user_id)

    if not user_db:
        raise HTTPException(status_code=404, detail=f'user item wuth id {user_id} not found')

    user = GetUserDTO(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email,
        is_active=user_db.is_active,
        blogs_subscriptions=user_db.blogs_subscriptions
    )

    return user


@router.post('/user/', response_model=CreateUserDTO, tags=['Tag'])
async def post_user(user: CreateUserDTO, session: AsyncSession = Depends(get_session)):
    user_db = get_and_create_user(session, user.username, user.email, user.password)

    await session.commit()
    return user_db


@router.put('/user/{user_id}', response_model=UpdateUserDTO, tags=['Tag'])
async def update_user(user_id: int, user: UpdateUserDTO, session: AsyncSession = Depends(get_session)):
    user_db = await get_and_update_user(session, user_id, user.username, user.email, user.password)

    if not user_db:
        raise HTTPException(status_code=404, detail=f'user item wuth id {user_id} not found')

    await session.commit()
    return user_db


@router.delete('/user/{user_id}', response_model=DeleteUserDTO, tags=['Tag'])
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await get_user(session, user_id)

    if not user_db:
        raise HTTPException(status_code=404, detail=f'user item wuth id {user_id} not found')

    await session.delete(user_db)
    await session.commit()
    return user_db
