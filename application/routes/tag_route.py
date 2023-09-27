from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from application.database import get_session
from application.schemas.tag_schems import GetTagsDTO, CreateTagDTO, GetTagDTO, UpdateTagDTO, DeleteTagDTO
from application.services.tag_services import get_tags, get_and_create_tag, get_and_update_tag, get_tag, \
    get_and_delete_tag

router = APIRouter()


@router.get('/tags/', response_model=list[GetTagsDTO], tags=['Tag'])
async def reads_tag(session: AsyncSession = Depends(get_session)):
    tag = await get_tags(session)

    if not tag:
        raise HTTPException(status_code=400, detail='Tag not found')

    tag = [
        GetTagsDTO(
            id=tag.id,
            tag_name=tag.tag_name,
        )
        for tag in tag
    ]

    return tag


@router.get('/tag/{tag_id}', response_model=GetTagDTO, tags=['Tag'])
async def read_tag(tag_id: int, session: AsyncSession = Depends(get_session)):
    tag = await get_tag(session, tag_id)

    if not tag:
        raise HTTPException(status_code=404, detail=f'tag item wuth id {tag_id} not found')

    tag = GetTagDTO(
        id=tag.id,
        tag_name=tag.tag_name,
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
    tag = await get_and_delete_tag(session, tag_id)

    if not tag:
        raise HTTPException(status_code=404, detail=f'tag item wuth id {tag_id} not found')

    await session.commit()
    return tag
