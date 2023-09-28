from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.blog import Blog
from application.models.user import User

from typing import Sequence, Type, List


async def get_blogs(session: AsyncSession) -> Sequence[Blog] | None:
    blogs_db = await session.execute(
        select(Blog)
        .options(selectinload(Blog.posts))
    )
    blogs_db = blogs_db.scalars().all()

    if not blogs_db:
        return None

    return blogs_db


async def get_and_create_blog(session: AsyncSession, title: str, description: str, owner_id: any) -> Blog | None:
    user = await session.get(User, owner_id)

    if not user:
        return None

    blog = Blog(title=title, description=description, owner_id=user.id)
    session.add(blog)

    return blog


async def get_blog(session: AsyncSession, blog_id: int) -> Type[Blog] | None:
    blog = await session.get(Blog, blog_id, options=[
            selectinload(Blog.authors),
            selectinload(Blog.subscribed_users),
            selectinload(Blog.posts)
    ])

    if not blog:
        return None

    return blog


async def get_and_update_blog(session: AsyncSession, blog_id: int, title: str, description: str, authors: List[any]) -> (Type[Blog] | None):

    blog = await session.get(Blog, blog_id, options=[
            selectinload(Blog.authors)
        ])

    if not blog:
        return None

    blog.title = title
    blog.description = description
    blog.authors = []

    await load_associated_property(authors, session, blog, 'authors', User)

    return blog


async def get_and_delete_blog(session: AsyncSession, blog_id: int) -> Type[Blog] | None:
    blog = await session.get(Blog, blog_id)

    if not blog:
        return None

    await session.delete(blog)

    return blog


async def load_associated_property(property_name, session, model, column_db: str, add_model):
    if property_name:
        for obg_id in property_name:
            obj_db = await session.get(add_model, obg_id)
            if obj_db:
                getattr(model, column_db).append(obj_db)
