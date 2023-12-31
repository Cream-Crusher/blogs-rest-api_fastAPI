from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.blog import Blog
from application.models.post import Post
from application.models.user import User

from typing import Sequence, Type, List

from application.services.services_extensions import load_associated_property


async def get_users(session: AsyncSession) -> Sequence[User] | None:
    users_db = await session.execute(select(User))
    users_db = users_db.scalars().all()

    if not users_db:
        return None

    return users_db


async def get_and_create_user(session: AsyncSession, username: str, email: str, password: str) -> User:
    user_db = User(username=username, email=email, password=password)
    session.add(user_db)

    return user_db


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    user_db = await session.execute(
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.blogs_subscriptions),
                 selectinload(User.blogs_authors),
                 selectinload(User.post_likes))
    )
    user_db = user_db.scalar()

    if not user_db:
        return None

    return user_db


async def get_and_update_user(session: AsyncSession, user_id: int, username: str, email: str, password: str, blogs_subscriptions: List[any] = None, blogs_authors: List[any] = None, post_likes: List[any] = None) -> \
        Type[User] | None:

    user_db = await session.get(User, user_id, options=[
            selectinload(User.blogs_subscriptions),
            selectinload(User.blogs_authors),
            selectinload(User.post_likes)
        ])

    if not user_db:
        return None

    user_db.email = email
    user_db.username = username
    user_db.password = password
    user_db.blogs_subscriptions = []
    user_db.post_likes = []
    user_db.blogs_authors = []

    await load_associated_property(post_likes, session, user_db, 'post_likes', Post)
    await load_associated_property(blogs_subscriptions, session, user_db, 'blogs_subscriptions', Blog)
    await load_associated_property(blogs_authors, session, user_db, 'blogs_authors', Blog)

    return user_db
