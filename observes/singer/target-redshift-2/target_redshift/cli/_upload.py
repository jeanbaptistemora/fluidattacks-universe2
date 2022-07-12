from ._core import (
    CmdContext,
    pass_ctx,
)
import click
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
)
from redshift_client.sql_client.connection import (
    connect,
    DbConnection,
    IsolationLvl,
)
from redshift_client.table.client import (
    TableClient,
)
from target_redshift import (
    loader,
)
from typing import (
    NoReturn,
)

LOG = logging.getLogger(__name__)


def _backup(schema: SchemaId) -> SchemaId:
    return SchemaId(f"{schema.name}_backup")


def _loading(schema: SchemaId) -> SchemaId:
    return SchemaId(f"{schema.name}_loading")


def _post_upload(client: SchemaClient, schema: SchemaId) -> Cmd[None]:
    _do_nothing = Cmd.from_cmd(lambda: None)
    drop_backup = client.exist(_backup(schema)).bind(
        lambda b: client.delete_cascade(_backup(schema)) if b else _do_nothing
    )
    rename_old = client.exist(schema).bind(
        lambda b: client.rename(schema, _backup(schema)) if b else _do_nothing
    )
    rename_loading = client.exist(_loading(schema)).bind(
        lambda b: client.rename(_loading(schema), schema) if b else _do_nothing
    )
    return drop_backup + rename_old + rename_loading


def _main(
    conn: DbConnection, schema: SchemaId, records_limit: int, truncate: bool
) -> Cmd[None]:
    client = new_client(conn, LOG)
    schema_client = client.map(SchemaClient)
    table_client = client.map(TableClient)
    recreate = schema_client.bind(
        lambda c: c.recreate_cascade(_loading(schema))
    )
    upload = table_client.bind(
        lambda c: loader.main(_loading(schema), c, records_limit, truncate)
    )
    post_upload = schema_client.bind(lambda c: _post_upload(c, schema))
    return recreate + upload + post_upload


@click.command()  # type: ignore[misc]
@click.option(
    "-s",
    "--schema-name",
    type=str,
    required=True,
    help="Schema name in your warehouse",
)
@click.option(
    "--records-limit",
    type=int,
    required=False,
    default=10000,
    help="Max # of records per group",
)
@click.option(
    "--truncate",
    type=bool,
    is_flag=True,
    help="Truncate records that exceed column size?",
)
@pass_ctx
def destroy_and_upload(
    ctx: CmdContext, schema_name: str, records_limit: int, truncate: bool
) -> NoReturn:
    _schema = SchemaId(schema_name)
    connection = connect(ctx.db_id, ctx.creds, False, IsolationLvl.AUTOCOMMIT)
    connection.bind(
        lambda c: _main(c, _schema, records_limit, truncate)
    ).compute()
