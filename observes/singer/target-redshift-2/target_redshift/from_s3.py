import boto3
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
import logging
from mypy_boto3_s3 import (
    S3Client,
    S3ServiceResource,
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
from target_redshift import (
    loader,
)
from target_redshift.input import (
    InputEmitter,
)
from target_redshift.loader import (
    S3Handler,
)
from target_redshift.strategy import (
    LoadingStrategy,
    Strategies,
)
from utils_logger_2 import (
    start_session,
)

LOG = logging.getLogger(__name__)


def _new_s3_client() -> Cmd[S3Client]:
    return Cmd.from_cmd(lambda: boto3.client("s3"))


def _new_s3_resource() -> Cmd[S3ServiceResource]:
    return Cmd.from_cmd(lambda: boto3.resource("s3"))


@dataclass(frozen=True)
class FromS3Executor:
    db_id: DatabaseId
    db_creds: Credentials
    schema_name: str
    bucket: str
    prefix: str
    role: str
    ignore_failed: bool

    def _upload_schema(
        self, client: SqlClient, table_client: TableClient, target: SchemaId
    ) -> Cmd[None]:
        _input = InputEmitter(self.ignore_failed).input_stream
        handler = _new_s3_client().bind(
            lambda c: _new_s3_resource().map(
                lambda r: S3Handler(
                    target, c, r, client, self.bucket, self.prefix, self.role
                )
            )
        )
        return handler.bind(
            lambda h: loader.from_s3(_input, target, table_client, h)
        )

    def _main(self, new_client: Cmd[SqlClient]) -> Cmd[None]:
        _schema = SchemaId(self.schema_name)
        table_client = new_client.map(TableClient)
        strategy: Cmd[LoadingStrategy] = new_client.map(Strategies).map(
            lambda s: s.recreate_all_schema(_schema)
        )

        return strategy.bind(
            lambda ls: table_client.bind(
                lambda tc: ls.main(
                    lambda s: new_client.bind(
                        lambda c: self._upload_schema(c, tc, s)
                    )
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
