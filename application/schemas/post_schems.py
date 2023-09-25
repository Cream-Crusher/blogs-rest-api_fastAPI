from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class GetBLogAuthorDTO(BaseModel):
    id: int


class PostBaseDTO(BaseModel):
    title: str
    body: str
    is_published: bool


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
