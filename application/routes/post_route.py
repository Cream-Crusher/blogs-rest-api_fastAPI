from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from application.database import get_session
from application.schemas.post_schems import CreatePostDTO, UpdatePostDTO, GetPostDTO, GetPostsDTO, DeletePostDTO, \
    GetBLogAuthorDTO
from application.services.post_services import get_and_create_post, get_and_update_post, get_post, get_posts, \
    get_and_delete_post

router = APIRouter()


@router.get('/posts/', response_model=list[GetPostsDTO], tags=['Post'])
async def read_posts(session: AsyncSession = Depends(get_session)):
    posts = await get_posts(session)

    if not posts:
        raise HTTPException(status_code=400, detail='Post not found')

    posts = [
        GetPostsDTO(
            id=post.id,
            title=post.title,
            body=post.body,
            is_published=post.is_published,
            created_at=post.created_at,
            views=post.views
        )
        for post in posts
    ]

    return posts


@router.get('/post/{post_id}', response_model=GetPostDTO, tags=['Post'])
async def read_post(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await get_post(session, post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f'post item wuth id {post_id} not found')

    author = GetBLogAuthorDTO(id=post.author.id, username=post.author.username)

    post = GetPostDTO(
        id=post.id,
        title=post.title,
        body=post.body,
        is_published=post.is_published,
        created_at=post.created_at,
        views=post.views,
        author=author
    )

    return post


@router.post('/post/', response_model=CreatePostDTO, tags=['Post'])
async def create_post(post: CreatePostDTO, session: AsyncSession = Depends(get_session)):
    post = await get_and_create_post(session, post.title, post.body, post.is_published, post.author_id)

    if not post:
        raise HTTPException(status_code=404, detail="User not found")

    await session.commit()

    post = CreatePostDTO(
        title=post.title,
        body=post.body,
        is_published=post.is_published,
        author_id=post.author_id
    )

    return post


@router.put('/post/{post_id}', response_model=UpdatePostDTO, tags=['Post'])
async def update_blog(post_id: int, post: UpdatePostDTO, session: AsyncSession = Depends(get_session)):
    post_db = await get_and_update_post(session, post_id, post.title, post.body, post.is_published)

    if not post_db:
        raise HTTPException(status_code=404, detail=f'Post item wuth id {post_id} not found')

    await session.commit()
    return post_db


@router.delete('/post/{post_id}', response_model=DeletePostDTO, tags=['Post'])
async def delete_blog(post_id: int, session: AsyncSession = Depends(get_session)):
    post = await get_and_delete_post(session, post_id)

    if not post:
        raise HTTPException(status_code=404, detail=f'Post item wuth id {post_id} not found')

    await session.commit()
    return post
