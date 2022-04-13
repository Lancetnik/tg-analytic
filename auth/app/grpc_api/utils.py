import logging

import click
import grpc

from .endpoints import Checker
from .schema import auth_pb2_grpc


logger = logging.getLogger("uvicorn.error")


def create_server(port):
    server = grpc.aio.server()
    auth_pb2_grpc.add_CheckerServicer_to_server(Checker(), server)
    listen_addr = f'[::]:{port}'

    message =  "Grpc running on %s"
    color_message = f"Grpc running on {click.style('%s', bold=True)}"
    logger.info(message, listen_addr, extra={"color_message": color_message})

    server.add_insecure_port(listen_addr)
    return server
