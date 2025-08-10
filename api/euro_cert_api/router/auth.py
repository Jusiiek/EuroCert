from fastapi import APIRouter, HTTPException, status, Depends

from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.authtentication.backend import AuthenticationBackend
from euro_cert_api.managers.user import UserManager
from euro_cert_api.schemas.auth import AuthCredentials


def get_auth_router(
    authenticator: Authenticator,
    authentication_backend: AuthenticationBackend,
    user_manager: UserManager
) -> APIRouter:

    router = APIRouter(prefix="/auth", tags=["auth"])

    get_current_user_and_token = authenticator.get_current_user_and_token()

    @router.post(
        "/login",
    )
    async def login(credentials: AuthCredentials):
        user = await user_manager.authenticate(credentials)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credentials.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not active.",
            )

        return await authentication_backend.login(user)



    return router
