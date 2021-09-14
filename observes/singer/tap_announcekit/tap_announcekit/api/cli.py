# pylint: skip-file
import click
from dataclasses import (
    dataclass,
)
import json
import logging
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from sgqlc import (
    codegen,
    introspection,
)
import sys
from tap_announcekit.api.auth import (
    Creds,
)
from tap_announcekit.api.client import (
    ApiClient,
)
import tempfile
from typing import (
    IO as IO_FILE,
    Optional,
)

LOG = logging.getLogger(__name__)


def _get_api_schema(target: IO_FILE[str]) -> IO[None]:
    client = ApiClient(Creds("", ""))
    data = client.endpoint(
        introspection.query,
        introspection.variables(
            include_description=False,
            include_deprecated=False,
        ),
    )
    json.dump(data, target, sort_keys=True, indent=4, default=str)
    target.write("\n")
    if data.get("errors"):
        sys.exit(1)
    return IO(None)


@dataclass(frozen=True)
class ArgsAdapter:
    def __init__(
        self,
        api_schema: IO_FILE[str],
        output_code: IO_FILE[str],
        schema_name: Optional[str] = None,
        docstrings: bool = False,
    ) -> None:
        object.__setattr__(self, "schema.json", api_schema)
        object.__setattr__(self, "schema.py", output_code)
        object.__setattr__(self, "schema_name", schema_name)
        object.__setattr__(self, "docstrings", docstrings)


def _gen_schema_code(
    api_schema: IO_FILE[str], output_code: IO_FILE[str]
) -> IO[None]:
    codegen.schema.handle_command(ArgsAdapter(api_schema, output_code))
    return IO(None)


@click.command()
@click.option("--out", type=click.File("w+"), default=sys.stdout)
def get_api_schema(out: IO_FILE[str]) -> IO[None]:
    return _get_api_schema(out)


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
            _get_api_schema(schema_file)
        schema_file.seek(0)
        LOG.info("Generating code")
        return _gen_schema_code(schema_file, out)
