from typing import Optional

from euro_cert_api.utils.models import CreateUpdateDictModel


class CreateTaskSchema(CreateUpdateDictModel):
    title: str
    description: Optional[str]


class UpdateTaskSchema(CreateTaskSchema):
    pass
