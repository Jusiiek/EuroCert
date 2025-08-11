from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.authtentication.backend import AuthenticationBackend
from euro_cert_api.managers.user import UserManager
from euro_cert_api.router.auth import get_auth_router


class Router:
    """
    The final instance that stores routers and their required parameters

    :param authenticator: Authenticator - Authenticator instance
    :param authentication_backend: AuthenticationBackend - AuthenticationBackend instance
    :param user_manager: UserManager - UserManager instance
    """

    def __init__(
            self,
            authenticator: Authenticator,
            authentication_backend: AuthenticationBackend,
            user_manager: UserManager
    ):
        self.authenticator = authenticator
        self.authentication_backend = authentication_backend
        self.user_manager = user_manager

    def get_auth_router(self):
        return get_auth_router(
            self.authenticator,
            self.authentication_backend,
            self.user_manager
        )
