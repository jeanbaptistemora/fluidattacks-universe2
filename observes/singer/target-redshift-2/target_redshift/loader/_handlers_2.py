# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    Cmd,
)
from fa_purity.json.transform import (
    dumps,
)
from fa_singer_io.singer import (
    SingerSchema,
    SingerState,
)
import logging
from mypy_boto3_s3 import (
    S3Client,
)
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.table.client import (
    TableClient,
)
from target_redshift.data_schema import (
    extract_table,
)
from tempfile import (
    TemporaryFile,
)

LOG = logging.getLogger(__name__)


class StateKeeperS3:
    _client: S3Client
    _bucket: str
    _obj_key: str

    def save(self, state: SingerState) -> Cmd[None]:
        def _action() -> None:
            LOG.info("Uploading new state")
            LOG.debug("Uploading state to %s/%s", self._bucket, self._obj_key)
            with TemporaryFile() as data:
                data.write(dumps(state.value).encode("UTF-8"))
                data.seek(0)
                self._client.upload_fileobj(data, self._bucket, self._obj_key)

        return Cmd.from_cmd(_action)


def create_table(
    client: TableClient, table_id: TableId, schema: SingerSchema
) -> Cmd[None]:
    table = extract_table(schema).unwrap()
    return client.new(table_id, table)
