from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str


class CreateUserDTO(UserSchema):
    password: str


class UserGet(UserSchema):
    id: int
    is_active: bool
