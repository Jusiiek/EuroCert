from datetime import datetime

from bson import ObjectId
from typing import Optional
from pydantic import Field

from euro_cert_api.models.base import Base


class Task(Base):
    title: str
    description: Optional[str]
    user_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tasks"

    @classmethod
    async def get_by_id(cls, task_id: ObjectId):
        return await cls.find({"_id": task_id}).first_or_none()

    @classmethod
    async def get_user_tasks(cls, user_id: ObjectId):
        return await cls.find({"user_id": user_id}).to_list()
