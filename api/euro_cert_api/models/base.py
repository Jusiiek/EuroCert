from bson import ObjectId
from beanie import Document
from pydantic import ConfigDict


class Base(Document):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
