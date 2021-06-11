import click
from target_redshift.loader import (
    load_data,
)
from typing import (
    IO,
)


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
    "-ds",
    "--drop-schema",
    is_flag=True,
    help="Flag to specify that you want to delete the schema if exist",
)
def main(auth: IO[str], schema_name: str, drop_schema: bool) -> None:
    load_data(auth, schema_name, drop_schema)
