import click
import json
from migrate_tables import (
    centralize_dynamo,
)
from typing import (
    IO,
)


@click.command()
@click.option("--schema", type=str, required=True)
@click.option("--dymo-tables", type=click.File("r"), required=True)
@click.option("--db-auth", type=click.File("r"), required=True)
def centralize_dynamo_schemas(
    schema: str, dymo_tables: IO[str], db_auth: IO[str]
) -> None:
    tables = json.load(dymo_tables)["tables"]
    centralize_dynamo.main(db_auth, tables, schema)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(centralize_dynamo_schemas)
