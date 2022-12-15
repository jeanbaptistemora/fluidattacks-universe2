import click
from code_etl import (
    upload_repo,
)
from code_etl.amend.actions import (
    start as start_amend,
)
from code_etl.arm import (
    ArmToken,
)
from code_etl.client import (
    Tables,
)
from code_etl.compute_bills import (
    main as bill_reports,
)
from code_etl.init_tables import (
    init_tables,
)
from code_etl.mailmap import (
    Mailmap,
    MailmapFactory,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    JsonValue,
)
from fa_purity.json.factory import (
    loads,
)
from fa_purity.json.value.transform import (
    Unfolder,
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
from redshift_client.id_objs import (
    SchemaId,
    TableId,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
import sys
from typing import (
    Any,
    IO as FILE,
    NoReturn,
    Optional,
    Tuple,
)


def creds_from_str(raw: str) -> Credentials:
    data = loads(raw).alt(Exception)
    user = data.bind(
        lambda x: Unfolder(JsonValue(x))
        .uget("user")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )
    password = data.bind(
        lambda x: Unfolder(JsonValue(x))
        .uget("password")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )
    return Credentials(user.unwrap(), password.unwrap())


def id_from_str(raw: str) -> DatabaseId:
    data = loads(raw).alt(Exception)
    name = data.bind(
        lambda x: Unfolder(JsonValue(x))
        .uget("name")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )
    host = data.bind(
        lambda x: Unfolder(JsonValue(x))
        .uget("host")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )
    port = data.bind(
        lambda x: Unfolder(JsonValue(x))
        .uget("port")
        .bind(lambda u: u.to_primitive(str).alt(Exception).map(int))
    )
    return DatabaseId(name.unwrap(), host.unwrap(), port.unwrap())


@dataclass(frozen=True)
class CmdContext:
    db_id: DatabaseId
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
pass_ctx = click.make_pass_decorator(CmdContext)  # type: ignore[misc]


def _get_mailmap(path: Optional[str]) -> Maybe[Mailmap]:
    return Maybe.from_optional(path).map(MailmapFactory.from_file_path)


def _to_table(pair: Tuple[str, str]) -> TableId:
    return TableId(SchemaId(pair[0]), pair[1])


@click.command()  # type: ignore[misc]
@click.option("--mailmap", type=mailmap_file)  # type: ignore[misc]
@click.option("--namespace", type=str, required=True)  # type: ignore[misc]
@click.pass_obj  # type: ignore[misc]
def amend_authors(
    ctx: CmdContext,
    mailmap: Optional[str],
    namespace: str,
) -> NoReturn:
    start_amend(
        ctx.db_id,
        ctx.creds,
        namespace,
        _get_mailmap(mailmap),
    ).compute()


@click.command()  # type: ignore[misc]
@click.argument("folder", type=str)  # type: ignore[misc]
@click.argument("year", type=int)  # type: ignore[misc]
@click.argument("month", type=int)  # type: ignore[misc]
@click.argument("integrates_token", type=str)  # type: ignore[misc]
def compute_bills(
    folder: str, year: int, month: int, integrates_token: str
) -> NoReturn:
    bill_reports(
        integrates_token, Path(folder), datetime(year, month, 1)
    ).compute()


@click.command()  # type: ignore[misc]
@click.option("--namespace", type=str, required=True)  # type: ignore[misc]
@click.option("--arm-token", type=str, required=True)  # type: ignore[misc]
@click.option("--mailmap", type=mailmap_file)  # type: ignore[misc]
@click.argument("repositories", type=str, nargs=-1)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def upload_code(
    ctx: CmdContext,
    namespace: str,
    arm_token: str,
    repositories: Tuple[str, ...],
    mailmap: Optional[str],
) -> NoReturn:
    # pylint: disable=too-many-arguments
    repos = tuple(Path(abspath(r)) for r in repositories)
    token = ArmToken.new(arm_token)
    upload_repo.upload_repos(
        ctx.db_id, ctx.creds, token, namespace, repos, _get_mailmap(mailmap)
    ).compute()


@click.group()  # type: ignore[misc]
def migration() -> None:
    # migration cli group
    pass


@click.command()  # type: ignore[misc]
@click.option(
    "--table",
    type=click.Choice([i.name for i in Tables], case_sensitive=False),
    required=True,
)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def init_table(
    ctx: CmdContext,
    table: str,
) -> NoReturn:
    # pylint: disable=too-many-arguments
    init_tables(
        ctx.db_id, ctx.creds, Tables.from_raw(table).unwrap()
    ).compute()


@click.group()  # type: ignore[misc]
@click.option("--db-id", type=click.File("r"), required=True)  # type: ignore[misc]
@click.option("--creds", type=click.File("r"), required=True)  # type: ignore[misc]
@click.pass_context  # type: ignore[misc]
def main(ctx: Any, db_id: FILE[str], creds: FILE[str]) -> None:  # type: ignore[misc]
    if "--help" not in sys.argv[1:]:
        ctx.obj = CmdContext(  # type: ignore[misc]
            id_from_str(db_id.read()),
            creds_from_str(creds.read()),
        )


main.add_command(amend_authors)
main.add_command(compute_bills)
main.add_command(init_table)
main.add_command(upload_code)
main.add_command(migration)
