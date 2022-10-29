# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    SingerLoader,
)
from ._handlers import (
    MutableTableMap,
    SingerHandler,
    SingerHandlerOptions,
)
from ._s3_loader import (
    S3Handler,
)
from dataclasses import (
    dataclass,
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


@dataclass(frozen=True)
class Loaders:
    @staticmethod
    def common_loader(
        client: TableClient, options: SingerHandlerOptions
    ) -> SingerLoader:
        state = MutableTableMap({})
        return SingerLoader.new(
            lambda s, p: SingerHandler(s, client, options).handle(state, p)
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