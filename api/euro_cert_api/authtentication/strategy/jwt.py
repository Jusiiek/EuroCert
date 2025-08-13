from typing import Optional

from fastapi import Header, HTTPException

from euro_cert_api.models.user import User
from euro_cert_api.models.blacklist_token import BlacklistToken
from euro_cert_api.managers.user import UserManager
from euro_cert_api.utils.jwt import (
    SecretType,
    JWT_ALGORITHM,
    decode_jwt,
    generate_jwt
)


class JWTStrategy:
    def __init__(
        self,
        secret: SecretType,
        lifetime: Optional[int],
        audience: str = "euro_cert:auth",
        algorithm: str = JWT_ALGORITHM
    ):
        self.secret = secret
        self.lifetime = lifetime
        self.audience = audience
        self.algorithm = algorithm

    async def read_token(
            self,
            token: Optional[str],
            user_manager: UserManager
    ) -> Optional[User]:
        if token is None:
            return None

        try:
            data = decode_jwt(
                token,
                self.secret,
                self.audience,
                [self.algorithm],
            )

            user_id = data.get("sub")
            if user_id is None:
                return None

        except Exception:
            return None

        try:
            parsed_id = user_manager.parse_id(user_id)
            return await user_manager.get_by_id(parsed_id)
        except Exception:
            return None

    async def write_token(
        self,
        user: User,
    ):
        data = {"sub": str(user.id), "aud": self.audience}
        return generate_jwt(
            data,
            self.secret,
            self.lifetime,
            self.algorithm,
        )

    async def destroy_token(self, token: str):
        await BlacklistToken.create(token=token)

    async def get_token(
        self,
        authorization: str = Header(None)
    ):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Invalid or missing authorization token"
            )
        return authorization[len("Bearer "):]
