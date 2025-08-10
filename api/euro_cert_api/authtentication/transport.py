from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from euro_cert_api.utils.models import model_to_dict


class BearerResponse(BaseModel):
    access_token: str
    token_type: str


class Transport:
    def __init__(self, tokenUrl: str):
        self.scheme = OAuth2PasswordBearer(tokenUrl, auto_error=False)

    async def get_login_response(self, token: str):
        res = BearerResponse(access_token=token, token_type="Bearer")
        return JSONResponse(model_to_dict(res))

    async def get_logout_response(self):
        pass
