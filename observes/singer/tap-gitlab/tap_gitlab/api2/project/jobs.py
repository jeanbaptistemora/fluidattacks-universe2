# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._core import (
    ProjectId,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from tap_gitlab.api2._raw import (
    RawClient,
)
from tap_gitlab.api2._utils import (
    int_to_str,
)
from tap_gitlab.api2.job import (
    JobId,
)


@dataclass(frozen=True)
class JobClient:
    _client: RawClient
    _proj: ProjectId

    def cancel(self, job: JobId) -> Cmd[None]:
        proj_id: str = self._proj.to_str()
        job_id: str = int_to_str(job.job_id)
        return self._client.post(f"/projects/{proj_id}/jobs/{job_id}/cancel")
