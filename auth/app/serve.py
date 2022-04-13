import argparse

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from propan.config import settings

from db import connect_db, close_db
from api import api_router
from grpc_api.utils import create_server


app = FastAPI(title=settings.PROJECT_NAME)

parser = argparse.ArgumentParser()
parser.add_argument('--port', nargs='?', type=int, default=8000, help='the listening port')
args, unknown = parser.parse_known_args()
app.state.port = args.port


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup() -> None:
    await connect_db(rebuild=False)
    server = create_server(app.state.port + 1)
    app.state.grpc_server = server
    await server.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    await close_db()
    await app.state.grpc_server.stop(1)


app.include_router(api_router)
