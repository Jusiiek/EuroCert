from datetime import datetime

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends

from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.common import exceptions
from euro_cert_api.models.task import Task
from euro_cert_api.models.user import User
from euro_cert_api.schemas.task import CreateTaskSchema, UpdateTaskSchema
from euro_cert_api.managers.user import UserManager


def get_tasks_router(
    authenticator: Authenticator,
    user_manager: UserManager
) -> APIRouter:

    get_current_active_user = authenticator.get_current_user(is_active=True)
    router = APIRouter(
        prefix="/tasks", tags=["task"], dependencies=[Depends(get_current_active_user)]
    )

    async def get_task_or_404(id: str) -> Task:
        try:
            parsed_id = user_manager.parse_id(id)
            task: Optional[Task] = await Task.get_by_id(parsed_id)
            if task is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return task
        except (exceptions.TaskNotExists, exceptions.InvalidID) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

    @router.post("/")
    async def create_task(
            task_create_data: CreateTaskSchema,
            user: User = Depends(get_current_active_user)
    ):
        task_data = task_create_data.create_update_dict()
        task = Task(**task_data, user_id=user.id)
        await task.insert()

    @router.get("/")
    async def get_user_tasks(
            user: User = Depends(get_current_active_user)
    ):
        return await Task.get_user_tasks(user.id)

    @router.put("/{id}")
    async def update_task(
            task_update: UpdateTaskSchema,
            task: Task = Depends(get_task_or_404)
    ):
        task_data = task_update.create_update_dict()

        for key, value in task_data.items():
            setattr(task, key, value)

        setattr(task, "updated_at", datetime.now())
        await task.save()

    @router.delete("/{id}")
    async def delete_task(task: Task = Depends(get_task_or_404)):
        await task.delete()

    return router
