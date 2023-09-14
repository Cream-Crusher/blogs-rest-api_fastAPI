from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.database import get_session
from application.schemas.blog import GetBLogDTO, DeleteBlogDTO, CreateBlogDTO, UpdateBlogDTO, GetBLogsDTO
from application.services.blog_service import get_blog, get_and_post_blog, get_and_put_blog, get_blogs

router = APIRouter()


@router.get('/blogs/', response_model=list[GetBLogsDTO])
async def read_blogs(session: AsyncSession = Depends(get_session)):
    blogs_db = await get_blogs(session)

    if not blogs_db:
        raise HTTPException(status_code=400, detail=('Blog not found'))

    blogs_db = [
        GetBLogsDTO(
            id=blog.id,
            title=blog.title,
            description=blog.description,
            created_at=blog.created_at,
            updated_at=blog.updated_at,
        )
        for blog in blogs_db
    ]

    return blogs_db


@router.get('/blog/{blog_id}', response_model=GetBLogDTO)
async def read_blog(blog_id: int, session: AsyncSession = Depends(get_session)):
    blog = await get_blog(session, blog_id)

    if not blog:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    blog = GetBLogDTO(
        id=blog.id,
        title=blog.title,
        description=blog.description,
        created_at=blog.created_at,
        updated_at=blog.updated_at,
        subscribed_users=blog.subscribed_users
    )

    return blog


@router.post('/blog/', response_model=CreateBlogDTO)
async def post_blog(blog: CreateBlogDTO, session: AsyncSession = Depends(get_session)):
    blog_db = get_and_post_blog(session, blog.title, blog.description)

    await session.commit()
    return blog_db


@router.put('/blog/{blog_id}', response_model=UpdateBlogDTO)
async def update_blog(blog_id: int, blog: UpdateBlogDTO, session: AsyncSession = Depends(get_session)):
    blog_db = await get_and_put_blog(session, blog_id, blog.title, blog.description)

    if not blog_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    await session.commit()
    return blog_db


@router.delete('/blog/{blog_id}', response_model=DeleteBlogDTO)
async def delete_blog(blog_id: int, session: AsyncSession = Depends(get_session)):
    blog_db = await get_blog(session, blog_id)

    if not blog_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    await session.delete(blog_db)
    await session.commit()
    return blog_db
