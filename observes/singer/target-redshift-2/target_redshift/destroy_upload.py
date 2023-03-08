from __future__ import (
    annotations,
)

import boto3
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
    Credentials,
    DatabaseId,
    IsolationLvl,
)
from redshift_client.table.client import (
    TableClient,
)
from target_redshift._utils import (
    S3FileObjURI,
)
from target_redshift.input import (
    InputEmitter,
)
from target_redshift.loader import (
    Loaders,
    SingerHandlerOptions,
    StateKeeperS3,
)
from target_redshift.output import (
    OutputEmitter,
)
from target_redshift.strategy import (
    Strategies,
)
from typing import (
    FrozenSet,
)
from utils_logger_2 import (
    start_session,
)

LOG = logging.getLogger(__name__)


def _new_s3_client() -> Cmd[S3Client]:
    return Cmd.from_cmd(lambda: boto3.client("s3"))


@dataclass(frozen=True)
class DestroyUploadExecutor:
    db_id: DatabaseId
    db_creds: Credentials
    target: SchemaId
    options: SingerHandlerOptions
    records_limit: int
    state: Maybe[S3FileObjURI]
    persistent: Maybe[FrozenSet[str]]
    ignore_failed: bool

    @property
    def _new_keeper(self) -> Cmd[Maybe[StateKeeperS3]]:
        return self.state.map(
            lambda s: _new_s3_client()
            .map(lambda c: StateKeeperS3(c, s))
            .map(lambda x: Maybe.from_value(x))
        ).value_or(Cmd.from_cmd(lambda: Maybe.empty(StateKeeperS3)))

    def _upload(
        self,
        client: SqlClient,
        table_client: TableClient,
        keeper: Maybe[StateKeeperS3],
    ) -> Cmd[None]:
        _input = InputEmitter(self.ignore_failed).input_stream
        loader = Loaders.common_loader(table_client, self.options, keeper)
        strategies = Strategies(client)
        strategy = self.persistent.map(
            lambda pt: strategies.recreate_per_stream(self.target, pt)
        ).value_or(strategies.recreate_all_schema(self.target))
        return OutputEmitter(
            _input, loader, strategy, self.records_limit
        ).main()

    def _main(self, new_client: Cmd[SqlClient]) -> Cmd[None]:
        table_client = new_client.map(TableClient)
        return new_client.bind(
            lambda sql: table_client.bind(
                lambda table: self._new_keeper.bind(
                    lambda k: self._upload(sql, table, k)
                )
            )
        )

    def execute(self) -> Cmd[None]:
        connection = connect(
            self.db_id, self.db_creds, False, IsolationLvl.AUTOCOMMIT
        )
        return start_session() + connection.bind(
            lambda con: self._main(new_client(con, LOG))
        )
