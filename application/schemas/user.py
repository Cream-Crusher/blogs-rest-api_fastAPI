# from pydantic import BaseModel
#
#
# class UserBase(BaseModel):
#     username: str
#     email: str
#
#
# class CreateUserDTO(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool


from pydantic import BaseModel


class CitySchema(BaseModel):
    name: str
    population: int
