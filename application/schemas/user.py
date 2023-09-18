from pydantic import BaseModel
from typing import Optional, List, Any

from application.models.blog import Blog


class UserSchemaDTO(BaseModel):
    username: str
    email: str


class DeleteUserDTO(BaseModel):
    id: int


class CreateUserDTO(UserSchemaDTO):
    password: str


class UpdateUserDTO(UserSchemaDTO):
    password: str
    blogs_subscriptions: Optional[List[int]]


class GetUserDTO(UserSchemaDTO):
    id: int
    is_active: bool
    blogs_subscriptions: Optional[List[int]]


class GetUsersDTO(UserSchemaDTO):
    id: int
    is_active: bool
