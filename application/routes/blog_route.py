from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.database import get_session
from application.models.blog import Blog
from application.models.user import User
from application.schemas.blog_schems import GetBLogDTO, DeleteBlogDTO, CreateBlogDTO, UpdateBlogDTO, GetBLogsDTO, \
    GetBlogUsersDTO
from application.services.blog_service import get_blog, get_and_create_blog, get_and_update_blog, get_blogs

router = APIRouter()


@router.get('/blogs/', response_model=list[GetBLogsDTO], tags=['Blog'])
async def read_blogs(session: AsyncSession = Depends(get_session)):
    blogs_db = await get_blogs(session)

    if not blogs_db:
        raise HTTPException(status_code=400, detail='Blog not found')

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


@router.get('/blog/{blog_id}', response_model=GetBLogDTO, tags=['Blog'])
async def read_blog(blog_id: int, session: AsyncSession = Depends(get_session)):
    blog = await session.get(Blog, blog_id, options=[
            selectinload(Blog.authors),
            selectinload(Blog.subscribed_users)
    ])

    if not blog:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    blogs_subscriptions = [GetBlogUsersDTO(id=sub.id, username=sub.username) for sub in blog.subscribed_users]
    authors = [GetBlogUsersDTO(id=author.id, username=author.username) for author in blog.authors]
    posts = (id=blog.post_id) if blog.post_id else None

    blog = GetBLogDTO(
        id=blog.id,
        title=blog.title,
        description=blog.description,
        created_at=blog.created_at,
        updated_at=blog.updated_at,
        subscribed_users=blogs_subscriptions,
        authors=authors,
        owner=blog.owner_id,
        posts=posts
    )

    return blog


@router.post('/blog/', response_model=CreateBlogDTO, tags=['Blog'])
async def post_blog(blog: CreateBlogDTO, session: AsyncSession = Depends(get_session)):
    user_db = await session.get(User, blog.owner_id[0].id)

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    blog_db = await get_and_create_blog(session, blog.title, blog.description, user_db)

    await session.commit()
    return CreateBlogDTO(
        title=blog_db.title,
        description=blog_db.description,
        owner_id=blog.owner_id,
    )


@router.put('/blog/{blog_id}', response_model=UpdateBlogDTO, tags=['Blog'])
async def update_blog(blog_id: int, blog: UpdateBlogDTO, session: AsyncSession = Depends(get_session)):
    blog_db = await get_and_update_blog(session, blog_id, blog.title, blog.description, blog.authors, blog.post_id)

    if not blog_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    await session.commit()
    return UpdateBlogDTO(
        title=blog_db.title,
        description=blog_db.description,
        authors=blog.authors,
        post_id=blog.post_id
    )


@router.delete('/blog/{blog_id}', response_model=DeleteBlogDTO, tags=['Blog'])
async def delete_blog(blog_id: int, session: AsyncSession = Depends(get_session)):
    blog_db = await get_blog(session, blog_id)

    if not blog_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    await session.delete(blog_db)
    await session.commit()
    return blog_db
