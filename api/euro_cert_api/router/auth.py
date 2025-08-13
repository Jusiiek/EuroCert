from fastapi import APIRouter, HTTPException, status

from euro_cert_api.authtentication.backend import AuthenticationBackend
from euro_cert_api.managers.user import UserManager
from euro_cert_api.schemas.auth import AuthCredentials
from euro_cert_api.common import exceptions


def get_auth_router(
    authentication_backend: AuthenticationBackend,
    user_manager: UserManager
) -> APIRouter:

    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post("/login")
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

    @router.post("/register")
    async def register(credentials: AuthCredentials):
        try:
            await user_manager.create(credentials)

        except exceptions.UserAlreadyExists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists.",
            )

        except exceptions.InvalidPasswordException as pass_e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password {}.".format(pass_e.reason),
            )

    return router
