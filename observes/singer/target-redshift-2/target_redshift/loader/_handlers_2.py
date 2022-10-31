# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from fa_purity.json.transform import (
    dumps,
)
from fa_singer_io.singer import (
    SingerState,
)
import logging
from mypy_boto3_s3 import (
    S3Client,
)
from tempfile import (
    TemporaryFile,
)

LOG = logging.getLogger(__name__)


def save_state_on_s3(
    client: S3Client,
    bucket: str,
    obj_key: str,
    state: SingerState,
) -> Cmd[None]:
    def _action() -> None:
        LOG.info("Uploading new state")
        LOG.debug("Uploading state to %s/%s", bucket, obj_key)
        with TemporaryFile() as data:
            data.write(dumps(state.value).encode("UTF-8"))
            data.seek(0)
            client.upload_fileobj(data, bucket, obj_key)

    return Cmd.from_cmd(_action)
