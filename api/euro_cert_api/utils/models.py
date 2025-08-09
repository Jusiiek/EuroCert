from typing import Any

from pydantic import BaseModel


def model_to_dict(model: BaseModel, *args, **kwargs) -> dict[str, Any]:
    return model.model_dump(*args, **kwargs)


def model_validate(schema: BaseModel, obj: Any, *args, **kwargs) -> BaseModel:
    return schema.model_validate(obj, *args, **kwargs)


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return model_to_dict(
            self,
            exclude_unset=True,
            exclude={"id"}
        )
