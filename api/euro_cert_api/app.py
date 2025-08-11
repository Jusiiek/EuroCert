import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from euro_cert_api.middleware import jwt_middleware


def create_app() -> FastAPI:
    app = FastAPI()

    origins = ["localhost:3000"]
    app.middleware("http")(jwt_middleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    return app

app = create_app()


def run_dev_server():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    run_dev_server()
