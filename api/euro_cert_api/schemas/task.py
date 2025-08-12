from typing import Optional

from euro_cert_api.utils.models import CreateUpdateDictModel


class CreateTaskSchema(CreateUpdateDictModel):
    title: str
    description: Optional[str]
    user_id: str


class UpdateTaskSchema(CreateTaskSchema):
    user_id: Optional[str]
