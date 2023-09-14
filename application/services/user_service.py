from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.user import User

from typing import Sequence, Type


async def get_users(session: AsyncSession) -> Sequence[User] | None:
    users_db = await session.execute(select(User).limit(10))
    users_db = users_db.scalars().all()

    if not users_db:
        return None

    return users_db


def get_and_post_user(session: AsyncSession, username: str, email: str, password: str) -> User:
    user_db = User(username=username, email=email, password=password)
    session.add(user_db)

    return user_db


async def get_user(session: AsyncSession, user_id: int) -> Type[User] | None:
    user_db = await session.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.blogs_subscriptions))
    )
    user_db = user_db.scalar_one()

    if not user_db:
        return None

    return user_db


async def get_and_put_user(session: AsyncSession, user_id: int, username: str, email: str, password: str) -> \
        (Type[User] | None):

    user_db = await session.get(User, user_id)

    if not user_db:
        return None

    user_db.username = username
    user_db.email = email
    user_db.password = password

    return user_db
