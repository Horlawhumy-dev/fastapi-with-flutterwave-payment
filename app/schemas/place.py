from typing import Annotated


from pydantic import BaseModel, BeforeValidator, Field


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class PlaceCreate(BaseModel):

    name: str
    address: str


class Place(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    profile_id: PyObjectId = Field(default_factory=PyObjectId, alias="profile_id")
    name: str
    address: str
