import argparse
    
from fastapi import FastAPI

from api import api_router
from grpc_api.utils import create_server


app = FastAPI()

parser = argparse.ArgumentParser()
parser.add_argument('--port', nargs='?', type=int, default=8000, help='the listening port')
args, unknown = parser.parse_known_args()
app.state.port = args.port


@app.on_event("startup")
async def startup() -> None:
    server = create_server(app.state.port + 1)
    app.state.grpc_server = server
    await server.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    await app.state.grpc_server.stop(1)


app.include_router(api_router)
