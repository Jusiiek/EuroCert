from euro_cert_api.utils.models import CreateUpdateDictModel


class AuthCredentials(CreateUpdateDictModel):
    email: str
    password: str
