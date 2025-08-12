from fastapi import APIRouter, HTTPException, status, Depends

from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.common import exceptions
from euro_cert_api.models.task import Task
from euro_cert_api.schemas.task import CreateTaskSchema, UpdateTaskSchema
from euro_cert_api.managers.task import TaskManager


def get_tasks_router(
    authenticator: Authenticator,
    task_manager: TaskManager
)-> APIRouter:

    get_current_active_user = authenticator.get_current_user(is_active=True)
    router = APIRouter(prefix="/tasks", tags=["task"], dependencies=[Depends(get_current_active_user)])


    async def get_task_or_404(id: str) -> Task:
        try:
            parsed_id = task_manager.parse_id(id)
            return await task_manager.get(parsed_id)
            pass
        except (exceptions.TaskNotExists, exceptions.InvalidID) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


    @router.post("/")
    async def create_task(task_data: CreateTaskSchema):
        pass


    @router.get("/")
    async def get_user_tasks():
        pass


    @router.put("/{id}")
    async def update_task(task: UpdateTaskSchema):
        pass


    @router.delete("/{id}")
    async def delete_task():
        pass


    return router
