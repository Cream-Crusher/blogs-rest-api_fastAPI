from pydantic import BaseModel


class UserSchemaDTO(BaseModel):
    username: str
    email: str


class DeleteUserDTO(BaseModel):
    id: int


class CreateUserDTO(UserSchemaDTO):
    password: str


class GetUserDTO(UserSchemaDTO):
    id: int
    is_active: bool
