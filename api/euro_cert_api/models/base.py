from bson import ObjectId
from beanie import Document
from euro_cert_api.utils.models import CreateUpdateDictModel


class Base(Document, CreateUpdateDictModel):

    class Config:
        populate_defaults = True
        json_loads = {ObjectId: str}
