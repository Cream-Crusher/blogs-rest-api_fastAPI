from datetime import datetime
from pydantic import BaseModel


class PostBaseDTO(BaseModel):
    title: str
    body: str
    is_published: bool


class DeletePostDTO(BaseModel):
    id: int


class CreatePostDTO(PostBaseDTO):
    pass


class UpdatePostDTO(PostBaseDTO):
    pass


class GetPostsDTO(PostBaseDTO):
    id: int
    created_at: datetime
    views: int


class GetPostDTO(PostBaseDTO):
    id: int
    created_at: datetime
    views: int
