from datetime import timezone, timedelta, datetime

from jose import jwt
from pydantic import SecretStr
from typing import Union, Optional, Any


SecretType = Union[str, SecretStr]
JWT_ALGORITHM = "HS256"


def _get_secret_value(secret: SecretType) -> str:
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


def generate_jwt(
        data: dict,
        secret: SecretType,
        lifetime_seconds: Optional[int] = None,
        algorithm: str = JWT_ALGORITHM
) -> str:
    payload = data.copy()
    if lifetime_seconds is not None:
        expire = datetime.now(timezone.utc) + timedelta(seconds=lifetime_seconds)
        payload["exp"] = expire
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_jwt(
    encoded_jwt: str,
    secret: SecretType,
    audience: str,
    algorithms: list[str] = [JWT_ALGORITHM],
) -> dict[str, Any]:
    return jwt.decode(
        token=encoded_jwt,
        key=_get_secret_value(secret),
        audience=audience,
        algorithms=algorithms
    )
