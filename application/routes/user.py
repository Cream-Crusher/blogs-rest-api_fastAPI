from fastapi import Depends, APIRouter
from sqlalchemy.exc import IntegrityError
from application.database import get_session
from application.schemas.user import UserGet, CreateUserDTO

from sqlalchemy.ext.asyncio import AsyncSession
from application.service.user import add_user, get_user


router = APIRouter()


@router.get('/users/', response_model=list[UserGet])
async def read_users(session: AsyncSession = Depends(get_session)):
    users = await get_user(session)

    users_schema = [
        UserGet(id=user.id, username=user.username, email=user.email, is_active=user.is_active)
        for user in users
    ]

    return users_schema


@router.post('/user/')
async def post_user(user: CreateUserDTO, session: AsyncSession = Depends(get_session)):
    user = add_user(session, user.username, user.email, user.password)

    try:
        await session.commit()
        return user
    except IntegrityError as e:
        await session.rollback()
