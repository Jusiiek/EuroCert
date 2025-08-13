from datetime import datetime, timezone

from fastapi import Request, Response

from euro_cert_api.config import (
    SECRET_KEY,
    AUDIENCE
)


def get_token(headers):
    token = headers["Authorization"]
    token = token.replace("Bearer ", "")
    return token


def is_token_expired(token: str) -> bool:
    from euro_cert_api.utils.jwt import decode_jwt
    try:
        payload = decode_jwt(
            token,
            SECRET_KEY,
            AUDIENCE
        )

        exp = payload.get("exp")
        if exp is None:
            return True
        now = datetime.now(timezone.utc).timestamp()
        return now > exp

    except Exception as e:
        print("MIDDLEWARE TOKEN EXPIRED", e)
        return True


async def jwt_middleware(request: Request, call_next):
    if "Authorization" not in request.headers or "auth" in str(
        request.url.path
    ):
        return await call_next(request)

    from euro_cert_api.models.blacklist_token import BlacklistToken

    token = get_token(request.headers)
    black_listed_token = await BlacklistToken.get_by_token(token)

    if black_listed_token is not None:
        return Response("INVALID_TOKEN", status_code=401)

    if is_token_expired(token):
        token = BlacklistToken(token=token)
        await token.insert()
        return Response("EXPIRED TOKEN", status_code=401)

    return await call_next(request)
