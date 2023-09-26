from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.database import get_session
from application.models.post import Post
from application.models.user import User
from application.schemas.post_schems import CreatePostDTO, UpdatePostDTO, GetPostDTO, GetPostsDTO, DeletePostDTO, \
    GetBLogAuthorDTO
from application.services.post_services import get_and_create_post, get_and_update_post, get_post, get_posts

router = APIRouter()


@router.get('/posts/', response_model=list[GetPostsDTO], tags=['Post'])
async def read_posts(session: AsyncSession = Depends(get_session)):
    posts_db = await get_posts(session)

    if not posts_db:
        raise HTTPException(status_code=400, detail=('Post not found'))

    posts_db = [
        GetPostsDTO(
            id=post.id,
            title=post.title,
            body=post.body,
            is_published=post.is_published,
            created_at=post.created_at,
            views=post.views
        )
        for post in posts_db
    ]

    return posts_db


@router.get('/post/{post_id}', response_model=GetPostDTO, tags=['Post'])
async def read_post(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await session.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f'post item wuth id {post_id} not found')

    author = GetBLogAuthorDTO(id=post.author_id)

    post = GetPostDTO(
        id=post.id,
        title=post.title,
        body=post.body,
        is_published=post.is_published,
        created_at=post.created_at,
        views=post.views,
        author=[author]
    )

    return post


@router.post('/post/', response_model=CreatePostDTO, tags=['Post'])
async def create_post(post: CreatePostDTO, session: AsyncSession = Depends(get_session)):
    user_db = await session.get(User, post.author_id[0].id)

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    post_db = await get_and_create_post(session, post.title, post.body, post.is_published, user_db)

    await session.commit()
    return CreatePostDTO(
        title=post_db.title,
        body=post_db.body,
        is_published=post_db.is_published,
    )


@router.put('/post/{post_id}', response_model=UpdatePostDTO, tags=['Post'])
async def update_blog(post_id: int, post: UpdatePostDTO, session: AsyncSession = Depends(get_session)):
    post_db = await get_and_update_post(session, post_id, post.title, post.body, post.is_published)

    if not post_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {post_id} not found')

    await session.commit()
    return post_db


@router.delete('/post/{post_id}', response_model=DeletePostDTO, tags=['Post'])
async def delete_blog(post_id: int, session: AsyncSession = Depends(get_session)):
    post_db = await get_post(session, post_id)

    if not post_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {post_id} not found')

    await session.delete(post_db)
    await session.commit()
    return post_db
