# pylint: skip-file

import asyncio
import click
from code_etl import (
    amend_authors as amend,
    compute_bills as bills,
    upload,
)
from code_etl.migration import (
    calc_fa_hash,
    calc_fa_hash_2,
)
from os.path import (
    abspath,
)
from postgres_client.connection.decoder import (
    creds_from_str,
    id_from_str,
)
from postgres_client.ids import (
    SchemaID,
    TableID,
)
from returns.maybe import (
    Maybe,
)
import sys
from typing import (
    IO as FILE,
    Iterator,
    Optional,
    Tuple,
)


@click.command()
@click.argument("schema", type=str)
@click.argument("mailmap_path", type=str)
@click.argument("namespace", type=str)
def amend_authors(schema: str, mailmap_path: str, namespace: str) -> None:
    asyncio.run(amend.main(schema, mailmap_path, namespace))


@click.command()
@click.argument("folder", type=str)
@click.argument("year", type=int)
@click.argument("month", type=int)
@click.argument("integrates_token", type=str)
def compute_bills(
    folder: str, year: int, month: int, integrates_token: str
) -> None:
    bills.main(
        folder,
        year,
        month,
        integrates_token,
    )


mailmap_file = click.Path(
    exists=True,
    file_okay=True,
    dir_okay=False,
    writable=False,
    readable=True,
    resolve_path=True,
    allow_dash=False,
    path_type=str,
)


@click.command()
@click.argument("namespace", type=str)
@click.argument("repositories", type=str, nargs=-1)
@click.option("--mailmap", type=mailmap_file)
def upload_code(
    namespace: str, repositories: Tuple[str, ...], mailmap: Optional[str]
) -> None:
    repos: Iterator[str] = map(abspath, repositories)
    success: bool = asyncio.run(
        upload.main(Maybe.from_optional(mailmap), namespace, *repos)
    )
    sys.exit(0 if success else 1)


@click.command()
@click.argument("namespace", type=str)
@click.option("--db-id", type=click.File("r"), required=True)
@click.option("--creds", type=click.File("r"), required=True)
@click.option("--schema", type=str, required=True)
def calculate_fa_hash(
    namespace: str, db_id: FILE[str], creds: FILE[str], schema: str
) -> None:
    calc_fa_hash.start(
        id_from_str(db_id.read()),
        creds_from_str(creds.read()),
        SchemaID(schema),
        namespace,
    )


@click.command()
@click.option("--db-id", type=click.File("r"), required=True)
@click.option("--creds", type=click.File("r"), required=True)
@click.option("--source-schema", type=str, required=True)
@click.option("--source-table", type=str, required=True)
@click.option("--target-schema", type=str, required=True)
@click.option("--target-table", type=str, required=True)
def calculate_fa_hash_2(
    db_id: FILE[str],
    creds: FILE[str],
    source_schema: str,
    source_table: str,
    target_schema: str,
    target_table: str,
) -> None:
    calc_fa_hash_2.start(
        id_from_str(db_id.read()),
        creds_from_str(creds.read()),
        TableID(SchemaID(source_schema), source_table),
        TableID(SchemaID(target_schema), target_table),
    )


@click.group()
def migration() -> None:
    # main cli group
    pass


migration.add_command(calculate_fa_hash)
migration.add_command(calculate_fa_hash_2)


@click.group()
def main() -> None:
    # main cli group
    pass


main.add_command(amend_authors)
main.add_command(compute_bills)
main.add_command(upload_code)
main.add_command(migration)
