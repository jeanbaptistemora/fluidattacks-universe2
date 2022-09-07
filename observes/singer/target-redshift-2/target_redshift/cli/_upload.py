# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from target_redshift.loader import (
    LoadingStrategy,
    SingerHandlerOptions,
)
from typing import (
    NoReturn,
)
from utils_logger_2 import (
    start_session,
)

LOG = logging.getLogger(__name__)


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
    default=1000000,
    help="Max # of records per group",
)
@click.option(
    "--records-per-query",
    type=int,
    required=False,
    default=1000,
    help="Max # of records per sql query",
)
@click.option(
    "--threads",
    type=int,
    required=False,
    default=1000,
    help="# of threads for query upload",
)
@click.option(
    "--truncate",
    type=bool,
    is_flag=True,
    help="Truncate records that exceed column size?",
)
@pass_ctx
def destroy_and_upload(
    ctx: CmdContext,
    schema_name: str,
    records_limit: int,
    truncate: bool,
    records_per_query: int,
    threads: int,
) -> NoReturn:
    _schema = SchemaId(schema_name)

    def _main(conn: DbConnection) -> Cmd[None]:
        client = new_client(conn, LOG)
        schema_client = client.map(SchemaClient)
        table_client = client.map(TableClient)
        strategy = schema_client.map(lambda s: LoadingStrategy(_schema, s))
        options = SingerHandlerOptions(
            truncate,
            records_per_query,
            threads,
        )

        def _upload(target: SchemaId) -> Cmd[None]:
            return table_client.bind(
                lambda t: loader.main(target, t, records_limit, options)
            )

        return strategy.bind(lambda ls: ls.main(_upload))

    connection = connect(ctx.db_id, ctx.creds, False, IsolationLvl.AUTOCOMMIT)
    cmd: Cmd[None] = start_session() + connection.bind(_main)
    cmd.compute()
