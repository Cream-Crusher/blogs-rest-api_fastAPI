from fastapi import Depends, APIRouter, HTTPException

from application.database import get_session
from application.schemas.user_schems import GetUserDTO, CreateUserDTO, DeleteUserDTO, UpdateUserDTO, GetUsersDTO, \
    GetBlogsSubscriptionsDTO, GetBlogsAuthorsDTO, GetPostLikesDTO
from application.services.user_service import get_and_create_user, get_users, get_user, get_and_update_user

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get('/users/', response_model=list[GetUsersDTO], tags=['User'])
async def read_users(session: AsyncSession = Depends(get_session)):
    users = await get_users(session)

    if not users:
        raise HTTPException(status_code=400, detail='Users not found')

    users = [
        GetUsersDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )
        for user in users
    ]

    return users


@router.get('/user/{user_id}', response_model=GetUserDTO, tags=['User'])
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user(session, user_id)

    if not user:
        raise HTTPException(status_code=404, detail=f'user item wuth id {user_id} not found')

    blogs_subscriptions = [GetBlogsSubscriptionsDTO(id=sub.id, title=sub.title) for sub in user.blogs_subscriptions]
    blogs_authors = [GetBlogsAuthorsDTO(id=author.id, title=author.title) for author in user.blogs_authors]
    post_likes = [GetPostLikesDTO(id=post_like.id, title=post_like.title) for post_like in user.post_likes]

    user = GetUserDTO(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        blogs_subscriptions=blogs_subscriptions,
        blogs_authors=blogs_authors,
        post_likes=post_likes
    )

    return user


@router.post('/user/', response_model=CreateUserDTO, tags=['User'])
async def post_user(user: CreateUserDTO, session: AsyncSession = Depends(get_session)):
    user = await get_and_create_user(session, user.username, user.email, user.password)

    await session.commit()
    return user


@router.put('/user/{user_id}', response_model=UpdateUserDTO, tags=['User'])
async def update_user(user_id: int, user: UpdateUserDTO, session: AsyncSession = Depends(get_session)):
    user = await get_and_update_user(session, user_id, user.username, user.email, user.password, user.blogs_subscriptions, user.blogs_authors, user.post_likes)

    if not user:
        raise HTTPException(status_code=404, detail=f'user item wuth id {user_id} not found')

    await session.commit()

    blogs_authors = [blog.id for blog in user.blogs_authors]
    post_likes = [post.id for post in user.post_likes]
    blogs_subscriptions = [blog.id for blog in user.blogs_subscriptions]

    user = UpdateUserDTO(
        username=user.username,
        email=user.email,
        password=user.password,
        blogs_subscriptions=blogs_subscriptions,
        blogs_authors=blogs_authors,
        post_likes=post_likes
    )

    return user


@router.delete('/user/{user_id}', response_model=DeleteUserDTO, tags=['User'])
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_db = await get_user(session, user_id)

    if not user_db:
        raise HTTPException(status_code=404, detail=f'user item wuth id {user_id} not found')

    await session.delete(user_db)
    await session.commit()
    return user_db
