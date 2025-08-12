from datetime import datetime

from typing import Optional
from bson import ObjectId

from euro_cert_api.managers.base import BaseManager
from euro_cert_api.models.user import User
from euro_cert_api.models.task import Task
from euro_cert_api.schemas.task import (
    CreateTaskSchema,
    UpdateTaskSchema,
)
from euro_cert_api.common import exceptions


class TaskManager(BaseManager):
    def __init__(self):
        super(self, TaskManager).__init__()

    async def get_by_id(self, task_id: ObjectId):
        task: Optional[Task] = await Task.get_by_id(task_id)
        if task is None:
            raise exceptions.TaskNotExists()

        return task

    async def create_task(self, create_task: CreateTaskSchema):
        task_data = create_task.create_update_dict()
        task = Task(**task_data)
        await task.insert()

    async def delete_task(self, task: Task):
        await task.delete()

    async def list_of_user_tasks(self, user: User):
        return await Task.list_of_user_tasks(user.id)

    async def update_task(self, update_task: UpdateTaskSchema, task: Task):
        task_data = update_task.create_update_dict()

        for key, value in task_data.items():
            if key != "user_id":
                setattr(task, key, value)

        setattr(task, "updated_at", datetime.now())
        await task.save()
