from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models.blog import Blog
from application.models.comment import Comment

from typing import Sequence, Type


async def get_comments(session: AsyncSession) -> Sequence[Comment] | None:
    comments_db = await session.execute(select(Comment))
    comments_db = comments_db.scalars().all()

    if not comments_db:
        return None

    return comments_db


async def get_and_create_comment(session: AsyncSession, body: str, user_id: any, post_id: any) -> Comment:
    comment_db = Comment(body=body, author_id=user_id, post_id=post_id)
    session.add(comment_db)

    return comment_db


async def get_comment(session: AsyncSession, comment_id: int) -> Type[Comment] | None:
    comment = await session.get(Comment, comment_id, options=[
            selectinload(Comment.author),
            selectinload(Comment.post)
    ])
    if not comment:
        return None

    return comment


async def get_and_update_comment(session: AsyncSession, comment_id: int, body: str) -> (Type[Comment] | None):
    comment_db = await session.get(Comment, comment_id)

    if not comment_db:
        return None

    comment_db.body = body

    return comment_db


async def get_and_delete_blog(session: AsyncSession, blog_id: int) -> Type[Blog] | None:
    blog = await session.get(Blog, blog_id)

    if not blog:
        return None

    await session.delete(blog)

    return blog
