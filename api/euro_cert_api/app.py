import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from euro_cert_api.middleware import jwt_middleware
from euro_cert_api.db import init_db
from euro_cert_api.config import (
    ORIGINS,
    SECRET_KEY,
    TOKEN_LIFETIME,
    AUDIENCE,
    HOST,
    PORT
)

from euro_cert_api.authtentication.authenticator import Authenticator
from euro_cert_api.authtentication.transport import Transport
from euro_cert_api.authtentication.strategy.jwt import JWTStrategy
from euro_cert_api.authtentication.backend import AuthenticationBackend
from euro_cert_api.managers.user import UserManager
from euro_cert_api.router import Router

transport = Transport("auth/login")
strategy = JWTStrategy(SECRET_KEY, TOKEN_LIFETIME, AUDIENCE)
user_manager = UserManager()
authenticator = Authenticator(user_manager, strategy)
backend = AuthenticationBackend(transport, strategy)
router = Router(
    authenticator=authenticator,
    backend=backend,
    user_manager=user_manager
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("Database initialized")

    yield # replaces try finally

    print("Shutting down...")


def create_app(lifespan) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.middleware("http")(jwt_middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    app.include_router(router.get_auth_router())
    app.include_router(router.get_tasks_router())

    return app


app = create_app(lifespan=lifespan)


def run_dev_server():
    uvicorn.run(
        app,
        host=HOST,
        port=PORT
    )


if __name__ == "__main__":
    run_dev_server()
