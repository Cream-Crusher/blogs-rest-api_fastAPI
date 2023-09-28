from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.post import Post
from application.models.tag import Tag
from application.models.user import User

from typing import Sequence, Type

from application.services.services_extensions import load_associated_property


async def get_posts(session: AsyncSession) -> Sequence[Post] | None:
    posts = await session.execute(
        select(Post)
        .options(selectinload(Post.tags))
    )
    posts = posts.scalars().all()

    if not posts:
        return None

    return posts


async def get_and_create_post(session: AsyncSession, title: str, body: str, is_published: bool, author_id: any, blog_id: int) -> Post | None:
    user = await session.get(User, author_id)

    if not user:
        return None

    post = Post(title=title, body=body, is_published=is_published, author_id=user.id, blog_id=blog_id)
    session.add(post)

    return post


async def get_post(session: AsyncSession, post_id: int) -> Type[Post] | None:
    post = await session.get(Post, post_id, options=[
            selectinload(Post.author),
            selectinload(Post.blog),
            selectinload(Post.tags)
    ])

    if not post:
        return None

    return post


async def get_and_update_post(session: AsyncSession, post_id: int, title: str, body: str, is_published: bool, tags_ids: [any]) -> \
        (Type[Post] | None):

    post = await session.get(Post, post_id, options=[
        selectinload(Post.tags)
    ])

    if not post:
        return None

    post.title = title
    post.body = body
    post.is_published = is_published
    post.tags = []

    await load_associated_property(tags_ids, session, post, 'tags', Tag)

    return post


async def get_and_delete_post(session: AsyncSession, post_id: int) -> Type[Post] | None:
    post = await session.get(Post, post_id)

    if not post:
        return None

    await session.delete(post)

    return post
