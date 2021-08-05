import click
from os import (
    environ,
)
from returns.io import (
    IO,
)
import sys
from tap_announcekit import (
    utils,
)
from tap_announcekit.auth import (
    Creds,
)


def get_creds() -> Creds:
    return Creds(environ["ANNOUNCEKIT_USER"], environ["ANNOUNCEKIT_PASSWD"])


@click.command()
def get_api_schema() -> IO[None]:
    # schema is public no need for real creds
    return utils.get_api_schema(Creds("", ""), sys.stdout)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(get_api_schema)
