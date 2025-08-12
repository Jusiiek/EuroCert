from typing import Any
from bson import ObjectId


class BaseManager:
    def parse_id(self, id: Any) -> ObjectId:
        """
        Parse a value into a correct ID type.

        Params
        -------------------
        id: Any - model id as different type

        Returns
        --------------
        id: ObjectId - Model correct ID
        """

        if isinstance(id, ObjectId):
            return id
        try:
            return ObjectId(id)
        except Exception as e:
            raise e
