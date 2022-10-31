# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from ._core import (
    CmdContext,
    pass_ctx,
)
import click
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Maybe,
)
import logging
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.sql_client import (
    new_client,
    SqlClient,
)
from redshift_client.sql_client.connection import (
    connect,
    DbConnection,
    IsolationLvl,
)
from redshift_client.table.client import (
    TableClient,
)
from target_redshift.emitter import (
    Emitter,
)
from target_redshift.loader import (
    Loaders,
    SingerHandlerOptions,
    SingerLoader,
)
from target_redshift.strategy import (
    LoadingStrategy,
    Strategies,
)
from typing import (
    NoReturn,
)
from utils_logger_2 import (
    start_session,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class _Upload:
    client: SqlClient
    client_2: TableClient
    options: SingerHandlerOptions
    target: SchemaId
    records_limit: int

    @property
    def loader(self) -> SingerLoader:
        return Loaders.common_loader(
            self.client_2, self.options, Maybe.empty()
        )

    @property
    def strategy(
        self,
    ) -> LoadingStrategy:
        return Strategies(self.client).recreate_all_schema(self.target)

    def emit(self) -> Cmd[None]:
        return Emitter(self.loader, self.strategy, self.records_limit).main()

    @staticmethod
    def from_connection(
        conn: DbConnection,
        target: SchemaId,
        options: SingerHandlerOptions,
        records_limit: int,
    ) -> Cmd[_Upload]:
        client = new_client(conn, LOG)
        table_client = client.map(TableClient)
        return client.bind(
            lambda sql: table_client.map(
                lambda table: _Upload(
                    sql, table, options, target, records_limit
                )
            )
        )


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
    target = SchemaId(schema_name)
    options = SingerHandlerOptions(
        truncate,
        records_per_query,
        threads,
    )

    connection = connect(ctx.db_id, ctx.creds, False, IsolationLvl.AUTOCOMMIT)
    cmd: Cmd[None] = start_session() + connection.bind(
        lambda conn: _Upload.from_connection(
            conn, target, options, records_limit
        )
    ).bind(lambda u: u.emit())
    cmd.compute()
