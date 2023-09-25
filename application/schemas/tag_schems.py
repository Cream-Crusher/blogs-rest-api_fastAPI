from pydantic import BaseModel


class TagBaseDTO(BaseModel):
    tag_name: str


class DeleteTagDTO(BaseModel):
    id: int


class CreateTagDTO(TagBaseDTO):
    tag_name: str


class UpdateTagDTO(TagBaseDTO):
    pass


class GetTagsDTO(TagBaseDTO):
    id: int


class GetTagDTO(TagBaseDTO):
    id: int
