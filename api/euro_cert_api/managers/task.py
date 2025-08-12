from bson import ObjectId

from euro_cert_api.managers.base import BaseManager
from euro_cert_api.models.user import User
from euro_cert_api.models.task import Task
from euro_cert_api.schemas.task import (
    CreateTaskSchema,
    UpdateTaskSchema,
)


class TaskManager(BaseManager):
    def __init__(self):
        super(self, TaskManager).__init__()

    async def get(self, task_id: ObjectId):
        pass

    async def create_task(self, create_task: CreateTaskSchema):
        pass

    async def delete_task(self, task: Task):
        await task.delete()

    async def list_of_user_tasks(self, user: User):
        pass

    async def update_task(self, update_task: UpdateTaskSchema, task: Task):
        pass
