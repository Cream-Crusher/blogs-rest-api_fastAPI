from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.post import Post

from typing import Sequence, Type


async def get_posts(session: AsyncSession) -> Sequence[Post] | None:
    posts_db = await session.execute(select(Post).limit(10))
    posts_db = posts_db.scalars().all()

    if not posts_db:
        return None

    return posts_db


def get_and_create_post(session: AsyncSession, title: str, body: str, is_published: bool) -> Post:
    post_db = Post(title=title, body=body, is_published=is_published)
    session.add(post_db)

    return post_db


async def get_post(session: AsyncSession, post_id: int) -> Type[Post] | None:
    post_db = await session.get(Post, post_id)

    if not post_db:
        return None

    return post_db


async def get_and_update_blog(session: AsyncSession, post_id: int, title: str, body: str, is_published: bool) -> \
        (Type[Post] | None):

    post_db = await session.get(Post, post_id)

    if not post_db:
        return None

    post_db.title = title
    post_db.body = body
    post_db.is_published = is_published

    return post_db
