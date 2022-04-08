import click
from code_etl import (
    upload_repo,
)
from code_etl.amend.actions import (
    start as start_amend,
)
from code_etl.compute_bills import (
    legacy as bills,
)
from code_etl.mailmap import (
    Mailmap,
    MailmapFactory,
)
from code_etl.migration import (
    calc_fa_hash,
)
from dataclasses import (
    dataclass,
)
from fa_purity.maybe import (
    Maybe,
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
from typing import (
    Any,
    IO as FILE,
    NoReturn,
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


@click.command()  # type: ignore[misc]
@click.option("--mailmap", type=mailmap_file)
@click.option("--schema", type=str, required=True)
@click.option("--table", type=str, required=True)
@click.option("--namespace", type=str, required=True)
@click.pass_obj
def amend_authors(
    ctx: CmdContext,
    schema: str,
    table: str,
    mailmap: Optional[str],
    namespace: str,
) -> NoReturn:
    start_amend(
        ctx.db_id,
        ctx.creds,
        _to_table((schema, table)),
        namespace,
        _get_mailmap(mailmap),
    ).compute()


@click.command()  # type: ignore[misc]
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


@click.command()  # type: ignore[misc]
@click.option("--schema", type=str, required=True)
@click.option("--table", type=str, required=True)
@click.option("--namespace", type=str, required=True)
@click.option("--mailmap", type=mailmap_file)
@click.argument("repositories", type=str, nargs=-1)
@pass_ctx
def upload_code(
    ctx: CmdContext,
    schema: str,
    table: str,
    namespace: str,
    repositories: Tuple[str, ...],
    mailmap: Optional[str],
) -> NoReturn:
    # pylint: disable=too-many-arguments
    repos = tuple(Path(abspath(r)) for r in repositories)
    target = _to_table((schema, table))
    mmap = _get_mailmap(mailmap)
    upload_repo.upload_repos(
        ctx.db_id, ctx.creds, target, namespace, repos, mmap
    ).compute()


@click.command()  # type: ignore[misc]
@click.argument("namespace", type=str)
@click.option("--source", type=(str, str), help="schema-table pair")
@click.option("--target", type=(str, str), help="schema-table pair")
@pass_ctx
def calculate_fa_hash(
    ctx: CmdContext,
    source: Tuple[str, str],
    target: Tuple[str, str],
    namespace: str,
) -> NoReturn:
    calc_fa_hash.start(
        ctx.db_id, ctx.creds, _to_table(source), _to_table(target), namespace
    ).compute()


@click.group()  # type: ignore[misc]
def migration() -> None:
    # migration cli group
    pass


migration.add_command(calculate_fa_hash)


@click.group()  # type: ignore[misc]
@click.option("--db-id", type=click.File("r"), required=True)
@click.option("--creds", type=click.File("r"), required=True)
@click.pass_context
def main(ctx: Any, db_id: FILE[str], creds: FILE[str]) -> None:  # type: ignore[misc]
    if "--help" not in click.get_os_args():
        ctx.obj = CmdContext(  # type: ignore[misc]
            id_from_str(db_id.read()),
            creds_from_str(creds.read()),
        )


main.add_command(amend_authors)
main.add_command(compute_bills)
main.add_command(upload_code)
main.add_command(migration)
