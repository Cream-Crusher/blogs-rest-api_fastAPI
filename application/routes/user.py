from fastapi import Depends, APIRouter
from fastapi import HTTPException

from application.database import get_session
from application.schemas.user import GetUserDTO, CreateUserDTO, DeleteUserDTO
from application.service.user import get_and_post_user, get_users, get_user_by_id

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get('/users/', response_model=list[GetUserDTO])
async def read_users(session: AsyncSession = Depends(get_session)):
    users_db = await get_users(session)

    if not users_db:
        raise HTTPException(
            status_code=400, detail=("Users not found")
        )

    users_db = [
        GetUserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )
        for user in users_db
    ]

    return users_db


@router.post('/user/')
async def post_user(user: CreateUserDTO, session: AsyncSession = Depends(get_session)):
    user_db = get_and_post_user(session, user.username, user.email, user.password)

    try:
        await session.commit()
        return user_db
    except IntegrityError as e:
        await session.rollback()


@router.get('/user/{user_id}', response_model=GetUserDTO)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await get_user_by_id(session, user_id)

    if not user_db:
        raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')

    user = GetUserDTO(
        id=user_db.id,
        username=user_db.username,
        email=user_db.email,
        is_active=user_db.is_active
    )

    return user


@router.delete('/user/{user_id}', response_model=GetUserDTO)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await get_user_by_id(session, user_id)

    if user_db:
        await session.delete(user_db)
        await session.commit()
    else:
        raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')

