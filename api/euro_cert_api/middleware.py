from fastapi import Request, Response


def get_token(headers):
    token = headers["Authorization"]
    token = token.replace("Bearer ", "")
    return token


async def jwt_middleware(request: Request, call_next):
    if "Authorization" not in request.headers or "auth" in str(
        request.url.path
    ):
        return await call_next(request)
    token = get_token(request.headers)
    from euro_cert_api.models.blacklist_token import BlacklistToken

    black_listed_token = await BlacklistToken.get_by_token(token)
    if black_listed_token is not None:
        return Response("INVALID_TOKEN", status_code=401)
    return await call_next(request)
