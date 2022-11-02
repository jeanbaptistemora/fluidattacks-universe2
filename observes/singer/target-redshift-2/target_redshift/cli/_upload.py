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
import boto3
import click
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Maybe,
)
import logging
from mypy_boto3_s3.client import (
    S3Client,
)
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
from target_redshift._utils import (
    S3FileObjURI,
)
from target_redshift.emitter import (
    Emitter,
)
from target_redshift.loader import (
    Loaders,
    SingerHandlerOptions,
    SingerLoader,
    StateKeeperS3,
)
from target_redshift.strategy import (
    LoadingStrategy,
    Strategies,
)
from typing import (
    NoReturn,
    Optional,
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
    keeper: Maybe[StateKeeperS3]

    @property
    def loader(self) -> SingerLoader:
        return Loaders.common_loader(self.client_2, self.options, self.keeper)

    @property
    def strategy(
        self,
    ) -> LoadingStrategy:
        return Strategies(self.client).recreate_all_schema(self.target)

    def emit(self) -> Cmd[None]:
        return Emitter(self.loader, self.strategy, self.records_limit).main()

    @staticmethod
    def _new_s3_client() -> Cmd[S3Client]:
        return Cmd.from_cmd(lambda: boto3.client("s3"))

    @classmethod
    def from_connection(
        cls,
        conn: DbConnection,
        target: SchemaId,
        options: SingerHandlerOptions,
        records_limit: int,
        state: Maybe[S3FileObjURI],
    ) -> Cmd[_Upload]:
        client = new_client(conn, LOG)
        table_client = client.map(TableClient)
        keeper = state.map(
            lambda s: cls._new_s3_client()
            .map(lambda c: StateKeeperS3(c, s))
            .map(lambda x: Maybe.from_value(x))
        ).value_or(Cmd.from_cmd(lambda: Maybe.empty(StateKeeperS3)))
        return client.bind(
            lambda sql: table_client.bind(
                lambda table: keeper.map(
                    lambda k: _Upload(
                        sql, table, options, target, records_limit, k
                    )
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
@click.option(
    "--s3-state",
    type=str,
    required=False,
    default=None,
    help="S3 file obj URI to upload the state; e.g. s3://mybucket/folder/state.json",
)
@pass_ctx
def destroy_and_upload(
    ctx: CmdContext,
    schema_name: str,
    records_limit: int,
    truncate: bool,
    records_per_query: int,
    threads: int,
    s3_state: Optional[str],
) -> NoReturn:
    target = SchemaId(schema_name)
    options = SingerHandlerOptions(
        truncate,
        records_per_query,
        threads,
    )
    _state = (
        Maybe.from_optional(s3_state)
        .map(S3FileObjURI.from_raw)
        .map(lambda r: r.unwrap())
    )
    connection = connect(ctx.db_id, ctx.creds, False, IsolationLvl.AUTOCOMMIT)
    cmd: Cmd[None] = start_session() + connection.bind(
        lambda conn: _Upload.from_connection(
            conn, target, options, records_limit, _state
        )
    ).bind(lambda u: u.emit())
    cmd.compute()
