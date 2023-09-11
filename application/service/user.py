from sqlalchemy.ext.asyncio import AsyncSession
from application.models.user import User
from sqlalchemy import select


async def get_users(session: AsyncSession) -> list[User]:
    user_db = await session.execute(select(User).limit(10))

    return user_db.scalars().all()


def get_and_post_user(session: AsyncSession, username: str, email: str, password: str):
    user_db = User(username=username, email=email, password=password)
    session.add(user_db)

    return user_db


async def get_user(session: AsyncSession, user_id: int) -> User:
    user = select(User).filter(User.id == user_id)

    result = await session.execute(user)
    user = result.scalar_one_or_none()  # Получаем одного пользователя или None

    return user


async def get_and_put_user(session: AsyncSession, user_id: int, username: str, email: str, password: str):
    user_db = await session.get(User, user_id)

    if not user_db:
        return None

    # Update the user's information with the provided data
    user_db.username = username
    user_db.email = email
    user_db.password = password

    return user_db
