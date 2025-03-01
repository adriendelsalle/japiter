import typer
from typing import Optional

from .app import Jupyverse


cli = typer.Typer()


@cli.command()
def serve(
    host: str = "127.0.0.1",
    port: int = 8000,
    open_browser: Optional[bool] = True,
    frontend: str = "jupyter_lab",
    routers: str = "jupyverse.routers.contents,"
    "jupyverse.routers.kernels,"
    "jupyverse.routers.nbconvert,",
):
    Jupyverse(host, port, open_browser, frontend, routers).run()


if __name__ == "__main__":
    cli()
