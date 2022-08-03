from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from fa_singer_io.singer import (
    SingerSchema,
)
import logging
from mypy_boto3_s3 import (
    S3Client,
)
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.sql_client import (
    QueryValues,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    dynamic_query,
)
from typing import (
    Dict,
    Optional,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class S3Handler:
    _schema: SchemaId
    _client: S3Client
    _db_client: SqlClient
    _bucket: str
    _prefix: str
    _iam_role: str

    def handle_schema(self, schema: SingerSchema) -> Cmd[None]:
        stm = f"""
            COPY {{schema}}.{{table}} FROM %(data_file)s
            iam_role %(role)s ESCAPE NULL AS 'nan' TRUNCATECOLUMNS
        """
        identifiers: Dict[str, Optional[str]] = {
            "schema": self._schema.name,
            "table": schema.stream,
        }
        data_file = self._bucket + "/" + self._prefix + schema.stream
        args: Dict[str, PrimitiveVal] = {
            "data_file": data_file,
            "role": self._iam_role,
        }
        start = Cmd.from_cmd(
            lambda: LOG.info(
                "Appending data: %s -> %s.%s",
                data_file,
                self._schema.name,
                schema.stream,
            )
        )
        end = Cmd.from_cmd(
            lambda: LOG.info(
                "S3 data uploaded into %s.%s", self._schema.name, schema.stream
            )
        )
        return (
            start
            + self._db_client.execute(
                dynamic_query(stm, freeze(identifiers)),
                QueryValues(freeze(args)),
            )
            + end
        )
