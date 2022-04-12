import click
import uvicorn

from serve import app


@click.command(context_settings={"auto_envvar_prefix": "UVICORN"})
@click.option(
    "--host",
    type=str,
    default="0.0.0.0",
    help="Bind socket to this host.",
    show_default=True,
)
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Bind socket to this port.",
    show_default=True,
)
def main(host, port):
    app.state.port = port
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    main()