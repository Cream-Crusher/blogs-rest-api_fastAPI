from pydantic import BaseModel
from typing import Optional, List


class UserSchemaDTO(BaseModel):
    username: str
    email: str


class DeleteUserDTO(BaseModel):
    id: int


class CreateUserDTO(UserSchemaDTO):
    password: str


class GetBlogsSubscriptionsDTO(BaseModel):
    id: int
    title: str


class GetBlogsAuthorsDTO(BaseModel):
    id: int
    title: str


class GetPostLikesDTO(BaseModel):
    id: int
    title: str


class UpdateUserDTO(UserSchemaDTO):
    password: str
    blogs_subscriptions: Optional[List[int]]
    blogs_authors: Optional[List[int]]
    post_likes: Optional[List[int]]


class GetUserDTO(UserSchemaDTO):
    id: int
    is_active: bool
    blogs_subscriptions: List[GetBlogsSubscriptionsDTO] = None
    blogs_authors: List[GetBlogsAuthorsDTO] = None
    post_likes: List[GetPostLikesDTO] = None


class GetUsersDTO(UserSchemaDTO):
    id: int
    is_active: bool
