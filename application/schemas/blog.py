from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class BlogSchemaDTO(BaseModel):
    title: str
    description: str


class DeleteBlogDTO(BaseModel):
    id: int


class CreateBlogDTO(BlogSchemaDTO):
    pass


class UpdateBlogDTO(BlogSchemaDTO):
    pass


class GetBLogDTO(BlogSchemaDTO):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
