from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.database import get_session
from application.schemas.post_schems import CreatePostDTO, UpdatePostDTO, GetPostDTO, GetPostsDTO, DeletePostDTO
from application.services.post_services import get_and_post_post, get_and_put_blog, get_post, get_posts

router = APIRouter()


@router.get('/posts/', response_model=list[GetPostsDTO])
async def read_posts(session: AsyncSession = Depends(get_session)):
    posts_db = await get_posts(session)

    if not posts_db:
        raise HTTPException(status_code=400, detail=('Post not found'))
    print(type(posts_db[0].body))
    print('|'*30)
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


@router.get('/post/{post_id}', response_model=GetPostDTO)
async def read_post(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await get_post(session, post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {post_id} not found')

    post = GetPostDTO(
        id=post.id,
        title=post.title,
        body=post.body,
        is_published=post.is_published,
        created_at=post.created_at,
        views=post.views
    )

    return post


@router.post('/post/', response_model=CreatePostDTO)
async def post_blog(post: CreatePostDTO, session: AsyncSession = Depends(get_session)):
    post_db = get_and_post_post(session, post.title, post.body, post.is_published)
    print(post_db.body)
    await session.commit()
    print(post_db.body)

    return post_db


@router.put('/post/{post_id}', response_model=UpdatePostDTO)
async def update_blog(post_id: int, post: UpdatePostDTO, session: AsyncSession = Depends(get_session)):
    post_db = await get_and_put_blog(session, post_id, post.title, post.body, post.is_published)

    if not post_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {post_id} not found')

    await session.commit()
    return post_db


@router.delete('/post/{post_id}', response_model=DeletePostDTO)
async def delete_blog(post_id: int, session: AsyncSession = Depends(get_session)):
    post_db = await get_post(session, post_id)

    if not post_db:
        raise HTTPException(status_code=404, detail=f'blog item wuth id {post_id} not found')

    await session.delete(post_db)
    await session.commit()
    return post_db
