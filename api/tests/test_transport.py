import pytest
from fastapi.responses import JSONResponse
from fastapi import Response


@pytest.mark.asyncio
async def test_get_login_response(transport):
    response = await transport.get_login_response("TOKEN")

    assert isinstance(response, JSONResponse)
    assert response.body == b'{"access_token":"TOKEN","token_type":"Bearer"}'


@pytest.mark.asyncio
async def test_get_logout_response(transport):
    response: Response = await transport.get_logout_response()
    assert response.status_code == 401
