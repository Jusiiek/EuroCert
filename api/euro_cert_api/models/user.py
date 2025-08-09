from euro_cert_api.models.base import Base


class User(Base):
    email: str
    hashed_password: str
    is_active: bool = True

    class Settings:
        name = "users"


    @classmethod
    async def get_by_id(cls, user_id):
        return await cls.filter(id=user_id).first()

    @classmethod
    async def get_by_email(cls, email):
        return await cls.filter(email=email).first()
