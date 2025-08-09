from euro_cert_api.utils.models import CreateUpdateDictModel

class CreateUserSchema(CreateUpdateDictModel):
    email: str
    password: str


class UpdateUserSchema(CreateUserSchema):
    pass
