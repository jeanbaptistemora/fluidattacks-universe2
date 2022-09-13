# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    JsonValue,
    ResultE,
)
from fa_purity.frozen import (
    freeze,
)
from tap_gitlab.api2._raw import (
    RawClient,
)
from tap_gitlab.api2._raw.page import (
    Page,
)
from tap_gitlab.api2._utils import (
    int_to_str,
)
from tap_gitlab.api2.job import (
    Job,
    JobId,
)
from tap_gitlab.api2.project import (
    ProjectId,
)
from typing import (
    Callable,
    Dict,
)


@dataclass(frozen=True)
class JobClient:
    _client: RawClient
    _proj: ProjectId

    def _jobs_page(
        self,
        page: Page,
        decode_job: Callable[
            [JsonObj], ResultE[Job]
        ],  # TODO: replace with implementation
    ) -> Cmd[FrozenList[Job]]:
        raw_args: Dict[str, JsonValue] = {
            "page": JsonValue(page.page_num),
            "per_page": JsonValue(page.per_page),
        }
        return self._client.get_list(
            "/projects/" + self._proj.to_str() + "/jobs", freeze(raw_args)
        ).map(lambda js: tuple(decode_job(j).unwrap() for j in js))

    def cancel(self, job: JobId) -> Cmd[None]:
        proj_id: str = self._proj.to_str()
        job_id: str = int_to_str(job.job_id)
        return self._client.post(f"/projects/{proj_id}/jobs/{job_id}/cancel")
