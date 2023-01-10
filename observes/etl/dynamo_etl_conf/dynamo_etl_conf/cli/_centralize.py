from ._core import (
    CmdContext,
    pass_ctx,
)
import click
from dynamo_etl_conf import (
    centralize as centralize_module,
)
from fa_purity import (
    Cmd,
)
import logging
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.sql_client import (
    new_client,
    SqlClient,
)
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    IsolationLvl,
)
import sys
from typing import (
    Any,
    NoReturn,
)

LOG = logging.getLogger(__name__)


def _client(ctx: CmdContext) -> Cmd[SqlClient]:
    conn = connect(
        ctx.db_id,
        ctx.creds,
        False,
        IsolationLvl.AUTOCOMMIT,
    )
    return conn.bind(lambda c: new_client(c, LOG))


@click.command()  # type: ignore[misc]
@click.option("--schema", type=str, required=True)  # type: ignore[misc]
@click.option("--tables", type=str, required=True, help="dynamodb tables separated by coma")  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def dynamo_tables(
    ctx: CmdContext,
    schema: str,
    tables: str,
) -> NoReturn:
    _tables = tuple(tables.split(","))
    cmd: Cmd[None] = _client(ctx).bind(
        lambda c: centralize_module.merge_dynamo_tables(
            SchemaClient(c), frozenset(_tables), SchemaId(schema)
        )
    )
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.option("--schema-prefix", type=str, required=True)  # type: ignore[misc]
@click.option("--schema", type=str, required=True)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def parts(
    ctx: CmdContext,
    schema_prefix: str,
    schema: str,
) -> NoReturn:
    cmd: Cmd[None] = _client(ctx).bind(
        lambda c: centralize_module.merge_parts(
            SchemaClient(c), schema_prefix, SchemaId(schema)
        )
    )
    cmd.compute()


@click.command()  # type: ignore[misc]
@click.option("--schema", type=str, required=True, help="as in `dynamo_tables` args")  # type: ignore[misc]
@click.option("--tables", type=str, required=True, help="as in `dynamo_tables` args")  # type: ignore[misc]
@click.option("--parts-schema-prefix", type=str, required=True, help="as in `parts` args i.e. `schema-prefix`")  # type: ignore[misc]
@click.option("--parts-loading-schema", type=str, required=True, help="as in `parts` args i.e. `schema`")  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def main(
    ctx: CmdContext,
    schema: str,
    tables: str,
    parts_schema_prefix: str,
    parts_loading_schema: str,
) -> NoReturn:
    _tables = tuple(tables.split(","))
    cmd: Cmd[None] = (
        _client(ctx)
        .map(lambda c: SchemaClient(c))
        .bind(
            lambda c: centralize_module.main(
                c,
                frozenset(_tables),
                parts_schema_prefix,
                SchemaId(parts_loading_schema),
                SchemaId("dynamodb_integrates_vms"),
                SchemaId(schema),
            )
        )
    )
    cmd.compute()


@click.group()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--db-name",
    envvar="REDSHIFT_DATABASE",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-host",
    envvar="REDSHIFT_HOST",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-port",
    envvar="REDSHIFT_PORT",
    type=int,
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-user",
    envvar="REDSHIFT_USER",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-passwd",
    envvar="REDSHIFT_PASSWORD",
    required=True,
)
@click.pass_context  # type: ignore[misc]
def centralize(
    ctx: Any,
    db_name: str,
    db_host: str,
    db_port: int,
    db_user: str,
    db_passwd: str,
) -> None:
    if "--help" not in sys.argv[1:]:
        ctx.obj = CmdContext(  # type: ignore[misc]
            DatabaseId(db_name, db_host, db_port),
            Credentials(db_user, db_passwd),
        )


centralize.add_command(dynamo_tables)
centralize.add_command(parts)
centralize.add_command(main)
