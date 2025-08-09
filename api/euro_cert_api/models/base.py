from pydantic import BaseModel, Field
from bson import ObjectId

from euro_cert_api.models import PyObjectId


class Base(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_defaults = True
        arbitrary_types_allowed = True
        json_loads = {ObjectId: str}
