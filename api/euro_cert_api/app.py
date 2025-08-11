import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from euro_cert_api.middleware import jwt_middleware
from euro_cert_api.db import init_db
from euro_cert_api.config import (
    ORIGINS,
    SECRET_KEY,
    TOKEN_LIFETIME
)

from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.authtentication.transport import Transport
from euro_cert_api.authtentication.strategy.jwt import JWTStrategy
from euro_cert_api.authtentication.backend import AuthenticationBackend
from euro_cert_api.managers.user import UserManager
from euro_cert_api.router import Router


transport = Transport("auth/login")
strategy = JWTStrategy(SECRET_KEY, TOKEN_LIFETIME)
user_manager = UserManager()
authenticator = Authenticator(user_manager, strategy)
backend = AuthenticationBackend(transport, strategy)

router = Router(
    authenticator=authenticator,
    backend=backend,
    user_manager=user_manager
)


def create_app() -> FastAPI:
    app = FastAPI()

    app.middleware("http")(jwt_middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    return app


app = create_app()


def get_app_routers() -> None:
    app.include_router(router.get_auth_router())


@app.on_event("startup")
async def start_db():
    await init_db()


def run_dev_server():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    run_dev_server()
