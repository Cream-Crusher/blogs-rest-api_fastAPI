from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.database import get_session
from application.models.post import Post
from application.models.tag import Tag
from application.models.user import User
from application.schemas.post_schems import CreatePostDTO, UpdatePostDTO, GetPostDTO, GetPostsDTO, DeletePostDTO, \
    GetBLogAuthorDTO
from application.schemas.tag_schems import GetTagsDTO, CreateTagDTO, GetTagDTO, UpdateTagDTO, DeleteTagDTO
from application.services.post_services import get_and_create_post, get_and_update_blog, get_post, get_posts
from application.services.tag_services import get_tags, get_and_create_tag, get_and_update_tag, get_tag

router = APIRouter()


@router.get('/tags/', response_model=list[GetTagsDTO], tags=['Tag'])
async def reads_tag(session: AsyncSession = Depends(get_session)):
    tags_db = await get_tags(session)

    if not tags_db:
        raise HTTPException(status_code=400, detail=('Tag not found'))

    tags_db = [
        GetTagsDTO(
            id=tag.id,
            tag_name=tag.tag_name,
        )
        for tag in tags_db
    ]

    return tags_db


@router.get('/tag/{tag_id}', response_model=GetTagDTO, tags=['Tag'])
async def read_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    tag_db = await session.get(Tag, tag_id)

    if not tag_db:
        raise HTTPException(status_code=404, detail=f'tag item wuth id {tag_id} not found')

    tag = GetTagDTO(
        id=tag_db.id,
        tag_name=tag_db.tag_name,
    )

    return tag


@router.post('/tag/', response_model=CreateTagDTO, tags=['Tag'])
async def create_tag(tag: CreateTagDTO, session: AsyncSession = Depends(get_session)):
    tag_db = await get_and_create_tag(session, tag.tag_name)

    await session.commit()
    return CreateTagDTO(
        tag_name=tag_db.tag_name,
    )



@router.put('/tag/{tag_id}', response_model=UpdateTagDTO, tags=['Tag'])
async def update_tag(tag_id: int, tag: UpdateTagDTO, session: AsyncSession = Depends(get_session)):
    tag_db = await get_and_update_tag(session, tag_id, tag.tag_name)

    if not tag_db:
        raise HTTPException(status_code=404, detail=f'tag item wuth id {tag_id} not found')

    await session.commit()
    return tag_db


@router.delete('/tag/{tag_id}', response_model=DeleteTagDTO, tags=['Tag'])
async def delete_blog(tag_id: int, session: AsyncSession = Depends(get_session)):
    tag_db = await get_tag(session, tag_id)

    if not tag_db:
        raise HTTPException(status_code=404, detail=f'tag item wuth id {tag_id} not found')

    await session.delete(tag_db)
    await session.commit()
    return tag_db
