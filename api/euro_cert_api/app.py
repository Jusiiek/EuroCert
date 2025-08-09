import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI()

    origins = ["localhost:3000"]

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
