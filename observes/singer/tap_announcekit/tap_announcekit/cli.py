# pylint: skip-file
import click
import logging
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
import sys
from tap_announcekit import (
    utils,
)
from tap_announcekit.auth import (
    Creds,
)
import tempfile
from typing import (
    IO as IO_FILE,
    Optional,
)

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--out", type=click.File("w+"), default=sys.stdout)
def get_api_schema(out: IO_FILE[str]) -> IO[None]:
    return utils.get_api_schema(out)


@click.command()
@click.option("--api-schema", type=click.File("r"), default=None)
@click.option("--out", type=click.File("w+"), default=sys.stdout)
def update_schema(
    api_schema: Optional[IO_FILE[str]], out: IO_FILE[str]
) -> IO[None]:
    def open_schema() -> IO_FILE[str]:
        return Maybe.from_optional(api_schema).or_else_call(
            lambda: tempfile.NamedTemporaryFile("w+")
        )

    with open_schema() as schema_file:
        if not api_schema:
            LOG.info("Getting current schema")
            utils.get_api_schema(schema_file)
        schema_file.seek(0)
        LOG.info("Generating code")
        return utils.gen_schema_code(schema_file, out)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(get_api_schema)
main.add_command(update_schema)
