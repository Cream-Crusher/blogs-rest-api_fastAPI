from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.models.tag import Tag

from typing import Sequence, Type


async def get_tags(session: AsyncSession) -> Sequence[Tag] | None:
    tag_db = await session.execute(select(Tag))
    tag_db = tag_db.scalars().all()

    if not tag_db:
        return None

    return tag_db


async def get_and_create_tag(session: AsyncSession, tag_name: str) -> Tag:
    tag_db = Tag(tag_name=tag_name)
    session.add(tag_db)

    return tag_db


async def get_tag(session: AsyncSession, tag_id: int) -> Type[Tag] | None:
    tag_db = await session.get(Tag, tag_id)

    if not tag_db:
        return None

    return tag_db


async def get_and_update_tag(session: AsyncSession, tag_id: int, tag_name: str) -> (Type[Tag] | None):

    tag_db = await session.get(Tag, tag_id)

    if not tag_db:
        return None

    tag_db.tag_name = tag_name

    return tag_db
