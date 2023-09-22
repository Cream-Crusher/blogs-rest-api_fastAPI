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


class GetBlogAuthorsDTO(BaseModel):
    id: int


class GetBLogOwnerDTO(BaseModel):
    id: int


class GetPostDTO(BaseModel):
    id: int = None


class CreateBlogDTO(BlogBaseDTO):
    owner_id: List[GetBLogOwnerDTO] = None


class UpdateBlogDTO(BlogBaseDTO):
    authors: List[GetBlogAuthorsDTO] = None
    post_id: List[GetPostDTO] = None


class GetBLogsDTO(BlogBaseDTO):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class GetBLogDTO(BlogBaseDTO):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    subscribed_users: Optional[List[GetBlogUsersDTO]] = None
    authors: Optional[List[GetBlogUsersDTO]] = None
    owner: List[GetBLogOwnerDTO] = None
    posts: Optional[List[GetPostDTO]] = None
