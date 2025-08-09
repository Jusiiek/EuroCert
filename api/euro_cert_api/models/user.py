from euro_cert_api.models.base import Base
from euro_cert_api.utils.models import CreateUpdateDictModel


class User(CreateUpdateDictModel, Base):
    email: str
    hashed_password: str
    is_active: bool = True
