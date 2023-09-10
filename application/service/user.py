from application.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(session: AsyncSession) -> list[User]:
    user_db = await session.execute(select(User).limit(10))

    return user_db.scalars().all()


def add_user(session: AsyncSession, username: str, email: str, password: str):
    user_db = User(username=username, email=email, password=password)
    session.add(user_db)

    return user_db
