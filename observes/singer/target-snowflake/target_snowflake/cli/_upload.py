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
from target_snowflake import (
    loader,
)
from target_snowflake.loader import (
    LoadingStrategy,
    SingerHandlerOptions,
)
from target_snowflake.snowflake_client.db import (
    DbManager,
    SchemaId,
)
from target_snowflake.snowflake_client.root import (
    RootManager,
)
from target_snowflake.snowflake_client.schema import (
    SchemaManager,
)
from target_snowflake.snowflake_client.sql_client import (
    DatabaseId,
    DbConnection,
    DbConnector,
    Identifier,
)
from typing import (
    NoReturn,
)
from utils_logger_2 import (
    start_session,
)

LOG = logging.getLogger(__name__)


def _new_db_manager(
    conn: DbConnection, database: DatabaseId
) -> Cmd[DbManager]:
    return conn.cursor(LOG.getChild("db-manager")).map(
        lambda c: RootManager(c).db_manager(database)
    )


def _new_schema_manager(
    conn: DbConnection, database: DatabaseId, schema: SchemaId
) -> Cmd[SchemaManager]:
    return conn.cursor(LOG.getChild("schema-manager")).map(
        lambda c: RootManager(c).db_manager(database).schema_manager(schema)
    )


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "-s",
    "--schema-name",
    type=str,
    required=True,
    help="Schema name in your warehouse",
)
@click.option(  # type: ignore[misc]
    "--records-limit",
    type=int,
    required=False,
    default=1000000,
    help="Max # of records per group",
)
@click.option(  # type: ignore[misc]
    "--records-per-query",
    type=int,
    required=False,
    default=1000,
    help="Max # of records per sql query",
)
@click.option(  # type: ignore[misc]
    "--threads",
    type=int,
    required=False,
    default=1000,
    help="# of threads for query upload",
)
@pass_ctx  # type: ignore[misc]
def destroy_and_upload(
    ctx: CmdContext,
    schema_name: str,
    records_limit: int,
    records_per_query: int,
    threads: int,
) -> NoReturn:
    schema = SchemaId(Identifier.from_raw(schema_name))
    database = ctx.db_id

    def _main(conn: DbConnection) -> Cmd[None]:
        manager = _new_db_manager(conn, database)
        strategy = manager.map(lambda m: LoadingStrategy(schema, m))
        options = SingerHandlerOptions(
            records_per_query,
            threads,
        )

        def _upload(target: SchemaId) -> Cmd[None]:
            return loader.main(
                lambda: _new_schema_manager(conn, database, target),
                records_limit,
                options,
            )

        return strategy.bind(lambda ls: ls.main(_upload))

    connector = DbConnector(ctx.creds)
    connection = connector.connect_db(ctx.db_id)
    cmd: Cmd[None] = start_session() + connection.bind(_main)
    cmd.compute()
