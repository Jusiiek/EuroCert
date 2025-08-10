from typing import Optional
from fastapi import Depends

from euro_cert_api.authtentication.strategy.jwt import JWTStrategy
from euro_cert_api.managers.user import UserManager
from euro_cert_api.models.user import User


class Authenticator:
    """
    It is responsible for handling authentication

    :param user_manager: UserManager instance
    :param strategy: JWTStrategy instance
    """

    def __init__(
        self,
        user_manager: UserManager,
        strategy: JWTStrategy
    ):
        self.user_manager = user_manager
        self.strategy = strategy

    async def _authenticate(
        self,
        token: str = None,
        is_active: bool = False,
    ) -> tuple[Optional[User], Optional[str]]:
        pass

    def get_current_user_and_token(self, is_active: bool = False):
        async def current_user_and_token_dependency(
            token: str = Depends(self.strategy.get_token)
        ) -> tuple[Optional[User], Optional[str]]:
            return await self._authenticate(token=token, is_active=is_active)

        return current_user_and_token_dependency

    def get_current_user(self, is_active: bool = False):
        async def current_user_dependency(
            token: str = Depends(self.strategy.get_token)
        ) -> Optional[User]:
            user, _ = await self._authenticate(token=token, is_active=is_active)
            return user

        return current_user_dependency
