from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from application.database import get_session
from application.schemas.blog_schems import GetBLogDTO, DeleteBlogDTO, CreateBlogDTO, UpdateBlogDTO, GetBLogsDTO, \
    GetBlogUsersDTO
from application.services.blog_service import get_blog, get_and_create_blog, get_and_update_blog, get_blogs, \
    get_and_delete_blog

router = APIRouter()


@router.get('/blogs/', response_model=list[GetBLogsDTO], tags=['Blog'])
async def read_blogs(session: AsyncSession = Depends(get_session)):
    blogs = await get_blogs(session)

    if not blogs:
        raise HTTPException(status_code=400, detail='Blog not found')

    blogs = [
        GetBLogsDTO(
            id=blog.id,
            title=blog.title,
            description=blog.description,
            created_at=blog.created_at,
            updated_at=blog.updated_at,
            posts_ids=blog.posts
        )
        for blog in blogs
    ]

    return blogs


@router.get('/blog/{blog_id}', response_model=GetBLogDTO, tags=['Blog'])
async def read_blog(blog_id: int, session: AsyncSession = Depends(get_session)):
    blog = await get_blog(session, blog_id)

    if not blog:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    blogs_subscriptions = [GetBlogUsersDTO(id=sub.id, username=sub.username) for sub in blog.subscribed_users]
    authors = [GetBlogUsersDTO(id=author.id, username=author.username) for author in blog.authors]
    posts = blog.posts if blog.posts else None

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
    blog = await get_and_create_blog(session, blog.title, blog.description, blog.owner_id)

    if not blog:
        raise HTTPException(status_code=404, detail="User not found")

    await session.commit()
    return CreateBlogDTO(
        title=blog.title,
        description=blog.description,
        owner_id=blog.owner_id,
    )


@router.put('/blog/{blog_id}', response_model=UpdateBlogDTO, tags=['Blog'])
async def update_blog(blog_id: int, blog: UpdateBlogDTO, session: AsyncSession = Depends(get_session)):
    blog_db = await get_and_update_blog(session, blog_id, blog.title, blog.description, blog.authors)

    if not blog_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    await session.commit()
    return UpdateBlogDTO(
        title=blog_db.title,
        description=blog_db.description,
        authors=blog.authors
    )


@router.delete('/blog/{blog_id}', response_model=DeleteBlogDTO, tags=['Blog'])
async def delete_blog(blog_id: int, session: AsyncSession = Depends(get_session)):
    blog_db = await get_and_delete_blog(session, blog_id)

    if not blog_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {blog_id} not found')

    await session.commit()
    return blog_db
