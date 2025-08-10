from fastapi import Response, status
from fastapi.responses import JSONResponse

from euro_cert_api.authtentication.strategy.jwt import JWTStrategy
from euro_cert_api.authtentication.transport import Transport
from euro_cert_api.models.user import User


class AuthenticationBackend:
    def __init__(self, transport: Transport, strategy: JWTStrategy):
        self.transport = transport
        self.strategy = strategy

    async def login(self, user: User) -> JSONResponse:
        token = await self.strategy.write_token(user)
        return await self.transport.get_login_response(token)

    async def logout(self, token) -> Response:
        await self.strategy.destroy_token(token)
        try:
            response = await self.transport.get_logout_response()
        except Exception:
            response = Response(status_code=status.HTTP_401_UNAUTHORIZED)
        return response
