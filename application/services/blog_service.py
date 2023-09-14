from sqlalchemy.ext.asyncio import AsyncSession
from application.models.blog import Blog
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.blog import Blog

from typing import Sequence, Type


async def get_blogs(session: AsyncSession) -> Sequence[Blog] | None:
    blogs_db = await session.execute(select(Blog).limit(10))
    blogs_db = blogs_db.scalars().all()

    if not blogs_db:
        return None

    return blogs_db


def get_and_post_blog(session: AsyncSession, title: str, description: str) -> Blog:
    blog_db = Blog(title=title, description=description)
    session.add(blog_db)

    return blog_db


async def get_blog(session: AsyncSession, blog_id: int) -> Type[Blog] | None:
    blog_db = await session.execute(
        select(Blog)
        .where(Blog.id == blog_id)
        .options(selectinload(Blog.subscribed_users))
    )
    blog_db = blog_db.scalar_one()

    if not blog_db:
        return None

    return blog_db


async def get_and_put_blog(session: AsyncSession, blog_id: int, title: str, description: str) -> \
        (Type[Blog] | None):

    blog_db = await session.get(Blog, blog_id)

    if not blog_db:
        return None

    blog_db.title = title
    blog_db.description = description

    return blog_db
