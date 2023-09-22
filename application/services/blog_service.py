from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.blog import Blog
from application.models.user import User

from typing import Sequence, Type, List


async def get_blogs(session: AsyncSession) -> Sequence[Blog] | None:
    blogs_db = await session.execute(select(Blog))
    blogs_db = blogs_db.scalars().all()

    if not blogs_db:
        return None

    return blogs_db


async def get_and_create_blog(session: AsyncSession, title: str, description: str, user_db: any) -> Blog:
    blog_db = Blog(title=title, description=description, owner_id=user_db.id)
    session.add(blog_db)

    return blog_db


async def get_blog(session: AsyncSession, blog_id: int) -> Blog | None:
    blog_db = await session.execute(
        select(Blog)
        .where(Blog.id == blog_id)
        .options(selectinload(Blog.subscribed_users))
    )
    blog_db = blog_db.scalar_one()

    if not blog_db:
        return None

    return blog_db


async def get_and_update_blog(session: AsyncSession, blog_id: int, title: str, description: str, authors: List[any],
                              post_id: List[any]) -> (Type[Blog] | None):

    blog_db = await session.get(Blog, blog_id, options=[
            selectinload(Blog.authors)
        ])

    if not blog_db:
        return None

    blog_db.title = title
    blog_db.description = description
    blog_db.authors = []
    blog_db.post_id = post_id if post_id[0].id else None

    await load_associated_property(authors, session, blog_db, 'authors')

    return blog_db


async def load_associated_property(property_name, session, model, column_db: str):
    if property_name:
        for obg_id in property_name:
            obj_db = await session.get(User, obg_id.id)
            getattr(model, column_db).append(obj_db)
