from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from application.database import get_session
from application.schemas.comment_schemas import GetCommentsDTO, CreateCommentDTO, GetCommentDTO, GetAuthorDTO, \
    GetPostDTO, UpdateCommentDTO, DeleteCommentDTO
from application.services.comment_service import get_comments, get_and_create_comment, get_and_update_comment, \
    get_comment

router = APIRouter()


@router.get('/comments/', response_model=list[GetCommentsDTO], tags=['Comment'])
async def read_comments(session: AsyncSession = Depends(get_session)):
    comments_db = await get_comments(session)

    if not comments_db:
        raise HTTPException(status_code=400, detail=('Comment not found'))

    comments_db = [
        GetCommentsDTO(
            id=comment.id,
            body=comment.body,
            author_id=comment.author_id,
            post_id=comment.post_id
        )
        for comment in comments_db
    ]

    return comments_db


@router.get('/comment/{comment_id}', response_model=GetCommentDTO, tags=['Comment'])
async def read_post(comment_id: int, session: AsyncSession = Depends(get_session)):
    comment = get_comment(session, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail=f'comment item wuth id {comment_id} not found')

    author = GetAuthorDTO(id=comment.author.id, username=comment.author.username)
    post = GetPostDTO(id=comment.post.id, title=comment.post.title)

    comment = GetCommentDTO(
        id=comment.id,
        body=comment.body,
        created_at=comment.created_at,
        author=author,
        post=post
    )

    return comment


@router.post('/comment/', response_model=CreateCommentDTO, tags=['Comment'])
async def create_comment(comment: CreateCommentDTO, session: AsyncSession = Depends(get_session)):
    comment_db = await get_and_create_comment(session, comment.body, comment.author_id, comment.post_id)

    await session.commit()

    return CreateCommentDTO(
        body=comment_db.body,
        author_id=comment_db.author_id,
        post_id=comment_db.post_id
    )


@router.put('/comment/{comment_id}', response_model=UpdateCommentDTO, tags=['Comment'])
async def update_blog(comment_id: int, post: UpdateCommentDTO, session: AsyncSession = Depends(get_session)):
    comment_db = await get_and_update_comment(session, comment_id, post.body)

    if not comment_db:
        raise HTTPException(status_code=404, detail=f'Comment item wuth id {comment_id} not found')

    await session.commit()
    return comment_db


@router.delete('/comment/{comment_id}', response_model=DeleteCommentDTO, tags=['Comment'])
async def delete_blog(comment_id: int, session: AsyncSession = Depends(get_session)):
    comment_db = await get_comment(session, comment_id)

    if not comment_db:
        raise HTTPException(status_code=404, detail=f'COmment item wuth id {comment_id} not found')

    await session.commit()
    return comment_db
