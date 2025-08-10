from typing import Optional

from euro_cert_api.models.user import User


class Authenticator:
    """
    It is responsible for handling authentication
    """

    async def _authenticate(
        self,
        token: str = None,
        is_active: bool = False,
    ) -> tuple[Optional[User], Optional[str]]:
        pass

    def get_current_user_and_token(self, is_active: bool = False):
        async def current_user_and_token_dependency(token: str) -> tuple[Optional[User], Optional[str]]:
            return await self._authenticate(token=token, is_active=is_active)

        return current_user_and_token_dependency

    def get_current_user(self, is_active: bool = False):
        async def current_user_dependency(token: str) -> Optional[User]:
            user, _ = await self._authenticate(token=token, is_active=is_active)
            return user

        return current_user_dependency
