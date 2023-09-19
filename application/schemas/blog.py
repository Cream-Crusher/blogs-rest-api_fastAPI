from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class BlogBaseDTO(BaseModel):
    title: str
    description: str


class DeleteBlogDTO(BaseModel):
    id: int


class CreateBlogDTO(BlogBaseDTO):
    pass


class UpdateBlogDTO(BlogBaseDTO):
    pass


class GetBLogsDTO(BlogBaseDTO):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class GetBLogDTO(BlogBaseDTO):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    subscribed_users: Optional[List[int]]


class GetBlogsSubscriptions(BaseModel):
    id: int
    title: str
