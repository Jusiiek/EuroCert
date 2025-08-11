from bson import ObjectId
from beanie import Document


class Base(Document):

    class Config:
        populate_defaults = True
        json_loads = {ObjectId: str}
