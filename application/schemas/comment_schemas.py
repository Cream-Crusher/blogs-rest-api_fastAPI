from datetime import datetime
from pydantic import BaseModel


class CommentBaseDTO(BaseModel):
    body: str


class DeleteCommentDTO(BaseModel):
    id: int


class GetAuthorDTO(BaseModel):
    id: int
    username: str


class GetPostDTO(BaseModel):
    id: int
    title: str


class CreateCommentDTO(CommentBaseDTO):
    author_id: int
    post_id: int


class UpdateCommentDTO(CommentBaseDTO):
    body: str


class GetCommentsDTO(CommentBaseDTO):
    id: int
    author_id: int
    post_id: int


class GetCommentDTO(CommentBaseDTO):
    id: int
    created_at: datetime
    author: GetAuthorDTO
    post: GetPostDTO
