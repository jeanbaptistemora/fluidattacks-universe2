# pylint: skip-file
import click
import re
from returns.maybe import (
    Maybe,
)
from target_redshift.loader import (
    load_data,
)
from target_redshift.singer_handlers import (
    StateId,
)
from typing import (
    IO,
    Optional,
)


class InvalidURI(Exception):
    pass


def _extract_s3_id(url: str) -> StateId:
    pattern = re.compile("s3://(.+)")
    path = pattern.match(url)
    if path:
        parts = path.group(1).split("/", 1)
        return StateId(parts[0], parts[1])
    raise InvalidURI()


@click.command()
@click.option(
    "-a",
    "--auth",
    type=click.File("r"),
    required=True,
    help="JSON authentication file",
)
@click.option(
    "-s",
    "--schema-name",
    type=str,
    required=True,
    help="Schema name in your warehouse",
)
@click.option(
    "--state",
    type=str,
    required=False,
    default=None,
    help="S3 URI to upload the state; e.g. s3://mybucket/folder/state.json",
)
@click.option(
    "-ds",
    "--drop-schema",
    is_flag=True,
    help="Flag to specify that you want to delete the schema if exist",
)
@click.option(
    "--old-ver",
    is_flag=True,
    help="Use old loader version",
)
def main(
    auth: IO[str],
    schema_name: str,
    drop_schema: bool,
    old_ver: bool,
    state: Optional[str],
) -> None:
    _state = Maybe.from_optional(state)
    load_data(
        auth,
        schema_name,
        drop_schema,
        old_ver,
        _state.map(_extract_s3_id).value_or(None),
    )
