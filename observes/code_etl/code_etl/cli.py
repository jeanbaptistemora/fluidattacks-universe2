# pylint: skip-file

import asyncio
import click
from code_etl import (
    amend as amend_v2,
    amend_authors as amend,
    compute_bills as bills,
    upload,
    upload_repo,
)
from code_etl.mailmap import (
    Mailmap,
    MailmapFactory,
)
from code_etl.migration import (
    calc_fa_hash,
    calc_fa_hash_2,
)
from dataclasses import (
    dataclass,
)
from os.path import (
    abspath,
)
from pathlib import (
    Path,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from postgres_client.connection.decoder import (
    creds_from_str,
    id_from_str,
)
from postgres_client.ids import (
    SchemaID,
    TableID,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
import sys
from typing import (
    Any,
    IO as FILE,
    Iterator,
    Optional,
    Tuple,
)


@dataclass(frozen=True)
class CmdContext:
    db_id: DatabaseID
    creds: Credentials


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
pass_ctx = click.make_pass_decorator(CmdContext)


def _get_mailmap(path: Optional[str]) -> Maybe[Mailmap]:
    return Maybe.from_optional(path).map(MailmapFactory.from_file_path)


def _to_table(pair: Tuple[str, str]) -> TableID:
    return TableID(SchemaID(pair[0]), pair[1])


@click.command()
@click.argument("schema", type=str)
@click.argument("mailmap_path", type=str)
@click.argument("namespace", type=str)
def amend_authors(schema: str, mailmap_path: str, namespace: str) -> None:
    asyncio.run(amend.main(schema, mailmap_path, namespace))


@click.command()
@click.option("--mailmap", type=mailmap_file)
@click.option("--schema", type=str, required=True)
@click.option("--table", type=str, required=True)
@click.option("--namespace", type=str, required=True)
@click.pass_obj
def amend_authors_v2(
    ctx: CmdContext,
    schema: str,
    table: str,
    mailmap: Optional[str],
    namespace: str,
) -> IO[None]:
    return amend_v2.start(
        ctx.db_id,
        ctx.creds,
        _to_table((schema, table)),
        namespace,
        _get_mailmap(mailmap),
    )


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
@click.option("--schema", type=str, required=True)
@click.option("--table", type=str, required=True)
@click.option("--namespace", type=str, required=True)
@click.option("--mailmap", type=mailmap_file)
@click.argument("repositories", type=str, nargs=-1)
@pass_ctx
def upload_code_v2(
    ctx: CmdContext,
    schema: str,
    table: str,
    namespace: str,
    repositories: Tuple[str, ...],
    mailmap: Optional[str],
) -> IO[None]:
    repos = tuple(Path(abspath(r)) for r in repositories)
    target = _to_table((schema, table))
    mmap = _get_mailmap(mailmap)
    return upload_repo.upload_repos(
        ctx.db_id, ctx.creds, target, namespace, repos, mmap
    )


@click.command()
@click.argument("namespace", type=str)
@click.option("--schema", type=str, required=True)
@pass_ctx
def calculate_fa_hash(
    ctx: CmdContext, namespace: str, schema: str
) -> IO[None]:
    return calc_fa_hash.start(
        ctx.db_id,
        ctx.creds,
        SchemaID(schema),
        namespace,
    )


@click.command()
@click.argument("namespace", type=str)
@click.option("--source", type=(str, str), help="schema-table pair")
@click.option("--target", type=(str, str), help="schema-table pair")
@pass_ctx
def calculate_fa_hash_2(
    ctx: CmdContext,
    source: Tuple[str, str],
    target: Tuple[str, str],
    namespace: str,
) -> IO[None]:
    return calc_fa_hash_2.start(
        ctx.db_id, ctx.creds, _to_table(source), _to_table(target), namespace
    )


@click.group()
def migration() -> None:
    # migration cli group
    pass


migration.add_command(calculate_fa_hash)
migration.add_command(calculate_fa_hash_2)


@click.group()
@click.option("--db-id", type=click.File("r"), required=True)
@click.option("--creds", type=click.File("r"), required=True)
@click.pass_context
def v2(ctx: Any, db_id: FILE[str], creds: FILE[str]) -> None:
    if "--help" not in click.get_os_args():
        ctx.obj = CmdContext(
            id_from_str(db_id.read()),
            creds_from_str(creds.read()),
        )


v2.add_command(upload_code_v2)
v2.add_command(amend_authors_v2)
v2.add_command(migration)


@click.group()
def main() -> None:
    # main cli group
    pass


main.add_command(amend_authors)
main.add_command(compute_bills)
main.add_command(upload_code)
main.add_command(v2)
