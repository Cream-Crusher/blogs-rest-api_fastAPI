from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.post import Post
from application.models.user import User

from typing import Sequence, Type


async def get_posts(session: AsyncSession) -> Sequence[Post] | None:
    posts = await session.execute(select(Post))
    posts = posts.scalars().all()

    if not posts:
        return None

    return posts


async def get_and_create_post(session: AsyncSession, title: str, body: str, is_published: bool, author_id: any) -> Post | None:
    user = await session.get(User, author_id)

    if not user:
        return None

    post = Post(title=title, body=body, is_published=is_published, author_id=user.id)
    session.add(post)

    return post


async def get_post(session: AsyncSession, post_id: int) -> Type[Post] | None:
    post = await session.get(Post, post_id, options=[
            selectinload(Post.author)
    ])

    if not post:
        return None

    return post


async def get_and_update_post(session: AsyncSession, post_id: int, title: str, body: str, is_published: bool) -> \
        (Type[Post] | None):

    post_db = await session.get(Post, post_id)

    if not post_db:
        return None

    post_db.title = title
    post_db.body = body
    post_db.is_published = is_published

    return post_db


async def get_and_delete_post(session: AsyncSession, post_id: int) -> Type[Post] | None:
    post = await session.get(Post, post_id)

    if not post:
        return None

    await session.delete(post)

    return post
