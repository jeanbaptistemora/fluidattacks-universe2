from ._common import (
    MutableTableMap,
    SingerHandler,
    SingerHandlerOptions,
)
from ._core import (
    SingerLoader,
)
from ._s3_loader import (
    S3Handler,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
)
from mypy_boto3_s3 import (
    S3Client,
    S3ServiceResource,
)
from redshift_client.sql_client import (
    SqlClient,
)
from redshift_client.table.client import (
    TableClient,
)
from target_redshift.loader._handlers import (
    StateKeeperS3,
)


@dataclass(frozen=True)
class Loaders:
    @staticmethod
    def common_loader(
        client: TableClient,
        options: SingerHandlerOptions,
        keeper: Maybe[StateKeeperS3],
    ) -> SingerLoader:
        state = MutableTableMap({})
        return SingerLoader.new(
            lambda s, p: SingerHandler(s, client, options, keeper).handle(
                state, p
            )
        )

    @staticmethod
    def s3_loader(
        _client: S3Client,
        _resource: S3ServiceResource,
        _db_client: SqlClient,
        _bucket: str,
        _prefix: str,
        _iam_role: str,
    ) -> SingerLoader:
        return SingerLoader.new(
            lambda s, p: S3Handler(
                s, _client, _resource, _db_client, _bucket, _prefix, _iam_role
            ).handle(p)
        )
