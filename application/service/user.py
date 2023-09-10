from application.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_users(session: AsyncSession) -> list[User]:
    user_db = await session.execute(select(User).limit(10))

    return user_db.scalars().all()


def add_user(session: AsyncSession, username: str, email: str, password: str):
    user_db = User(username=username, email=email, password=password)
    session.add(user_db)

    return user_db


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).filter(User.id == user_id)

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()  # Получаем одного пользователя или None

    return user




# def delete_user(id: int, session: Session = Depends(get_session)):
#     user = session.query(user_models.User).get(id)
#
#     if user:
#         session.delete(user)
#         session.commit()
#     else:
#         raise HTTPException(status_code=404, detail=f'user item wuth id {id} not found')