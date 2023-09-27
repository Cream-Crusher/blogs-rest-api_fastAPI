from datetime import datetime

from pydantic import BaseModel


class PostBaseDTO(BaseModel):
    title: str
    body: str
    is_published: bool


class GetPostAuthorDTO(BaseModel):
    id: int
    username: str


class DeletePostDTO(BaseModel):
    id: int


class GetBlogDTO(BaseModel):
    id: int
    title: str


class CreatePostDTO(PostBaseDTO):
    author_id: int
    blog_id: int


class UpdatePostDTO(PostBaseDTO):
    pass


class GetPostsDTO(PostBaseDTO):
    id: int
    created_at: datetime
    views: int
    blog_id: int


class GetPostDTO(PostBaseDTO):
    id: int
    created_at: datetime
    views: int
    author: GetPostAuthorDTO
    blog: GetBlogDTO
