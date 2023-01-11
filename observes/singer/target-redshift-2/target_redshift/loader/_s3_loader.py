from botocore.exceptions import (
    ClientError,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.utils import (
    raise_exception,
)
from fa_singer_io.singer import (
    SingerSchema,
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
    QueryValues,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    dynamic_query,
)
from target_redshift.grouper import (
    PackagedSinger,
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
    _resource: S3ServiceResource
    _db_client: SqlClient
    _bucket: str
    _prefix: str
    _iam_role: str

    def _exist(self, file: str) -> Cmd[bool]:
        def _action() -> bool:
            try:
                self._resource.Object(self._bucket, file).load()
            except ClientError as e:  # type: ignore[misc]
                if e.response["Error"]["Code"] == "404":  # type: ignore[misc]
                    return False
                else:
                    raise Exception(f"S3 error: {e.response}")  # type: ignore[misc]
            else:
                return True

        return Cmd.from_cmd(_action)

    def _upload(self, schema: SingerSchema, data_file: str) -> Cmd[None]:
        fields = (
            Unfolder(schema.schema.encode()["properties"])
            .to_json()
            .map(lambda d: frozenset(d))
            .unwrap()
        )
        order = tuple(sorted(fields))
        columns: Dict[str, str] = {
            f"column_{i}": v for i, v in enumerate(order)
        }
        columns_ids = ",".join(f"{{column_{i}}}" for i, _ in enumerate(order))
        stm = f"""
            COPY {{schema}}.{{table}} ({columns_ids}) FROM %(data_file)s
            iam_role %(role)s CSV NULL AS 'nan' TRUNCATECOLUMNS FILLRECORD
        """
        identifiers: Dict[str, str] = {
            "schema": self._schema.name,
            "table": schema.stream,
        } | columns
        args: Dict[str, PrimitiveVal] = {
            "data_file": "s3://" + self._bucket + "/" + data_file,
            "role": self._iam_role,
        }
        return self._db_client.execute(
            dynamic_query(stm, freeze(identifiers)),
            QueryValues(freeze(args)),
        )

    def handle_schema(self, schema: SingerSchema) -> Cmd[None]:
        data_file = self._prefix + schema.stream + ".csv"
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
        skip = Cmd.from_cmd(
            lambda: LOG.warning(
                "Ignoring nonexistent S3 file: %s",
                self._bucket + "/" + data_file,
            )
        )
        upload = start + self._upload(schema, data_file) + end
        return self._exist(data_file).bind(lambda b: upload if b else skip)

    def handle(self, item: PackagedSinger) -> Cmd[None]:
        ignored_records = Cmd.from_cmd(
            lambda: LOG.warning("S3 loader ignores supplied singer records")
        )
        return item.map(
            lambda _: ignored_records,
            self.handle_schema,
            lambda _: raise_exception(NotImplementedError()),
        )
