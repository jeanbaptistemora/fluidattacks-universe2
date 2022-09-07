# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    Stream,
)
from fa_purity.pure_iter.factory import (
    from_list,
    unsafe_from_cmd,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
)
from mypy_boto3_batch import (
    BatchClient,
)
from mypy_boto3_batch.literals import (
    JobStatusType,
)
from mypy_boto3_batch.type_defs import (
    JobSummaryTypeDef,
)


@dataclass(frozen=True)
class JobsClient:
    _client: BatchClient
    _queue: str

    def list_jobs(self, status: JobStatusType) -> Stream[JobSummaryTypeDef]:
        data = unsafe_from_cmd(
            Cmd.from_cmd(
                lambda: self._client.get_paginator("list_jobs").paginate(
                    jobQueue=self._queue,
                    jobStatus=status,
                )
            )
        ).map(lambda x: Cmd.from_cmd(lambda: from_list(x["jobSummaryList"])))
        return chain(from_piter(data))
