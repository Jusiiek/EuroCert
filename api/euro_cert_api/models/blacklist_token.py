from euro_cert_api.models.base import Base


class BlacklistToken(Base):
    token: str
    type: str = "Bearer"

    class Settings:
        name = "blacklist_tokens"

    @classmethod
    async def get_by_token(cls, token: str):
        return await cls.find({"token": token}).first_or_none()
