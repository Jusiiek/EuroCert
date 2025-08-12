from euro_cert_api.schemas.user import CreateUserSchema


class AuthCredentials(CreateUserSchema):
    email: str
    password: str
