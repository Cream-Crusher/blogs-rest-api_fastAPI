from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class BlogBaseDTO(BaseModel):
    title: str
    description: str


class DeleteBlogDTO(BaseModel):
    id: int


class GetBlogUsersDTO(BaseModel):
    id: int
    username: str


class CreateBlogDTO(BlogBaseDTO):
    owner_id: int = None


class UpdateBlogDTO(BlogBaseDTO):
    authors: Optional[List[int]] = None


class GetPost(BaseModel):
    id: int
    title: str


class GetBLogsDTO(BlogBaseDTO):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    posts_ids: Optional[List[int]] = None


class GetBLogDTO(BlogBaseDTO):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    subscribed_users: Optional[List[GetBlogUsersDTO]] = None
    authors: Optional[List[GetBlogUsersDTO]] = None
    owner: int = None
    posts: Optional[List[GetPost]] = None
