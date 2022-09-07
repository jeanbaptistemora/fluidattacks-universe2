# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _utils,
)
from .core import (
    RecordGroup,
)
from .csv import (
    save,
)
import boto3
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
import logging
from mypy_boto3_s3.client import (
    S3Client,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class S3FileUploader:
    _client: S3Client
    _bucket: str
    _prefix: str

    def upload_to_s3(self, group: RecordGroup) -> Cmd[None]:
        file = save(group)
        file_key = self._prefix + group.schema.stream + ".csv"
        msg = _utils.log_cmd(
            lambda: LOG.info(
                "Uploading stream `%s` -> s3://%s",
                group.schema.stream,
                self._bucket + "/" + file_key,
            ),
            None,
        )
        end = _utils.log_cmd(
            lambda: LOG.info(
                "s3://%s uploaded!",
                self._bucket + "/" + file_key,
            ),
            None,
        )
        return file.bind(
            lambda f: f.over_binary(
                lambda f: msg
                + Cmd.from_cmd(
                    lambda: self._client.upload_fileobj(
                        f, self._bucket, file_key
                    )
                )
                + end
            )
        )


def new_client() -> Cmd[S3Client]:
    return Cmd.from_cmd(lambda: boto3.client("s3"))
