from datetime import datetime
from typing import List

from pydantic import BaseModel


class PostBaseDTO(BaseModel):
    title: str
    body: str
    is_published: bool


class GetBLogAuthorDTO(BaseModel):
    id: int


class DeletePostDTO(BaseModel):
    id: int


class CreatePostDTO(PostBaseDTO):
    author_id: List[GetBLogAuthorDTO] = None


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
    author: List[GetBLogAuthorDTO] = None
