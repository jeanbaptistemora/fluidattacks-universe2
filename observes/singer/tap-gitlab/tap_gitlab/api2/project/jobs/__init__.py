# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0

from ._decode import (
    decode_job_id,
    decode_job_obj,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    JsonValue,
    Maybe,
    Stream,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_empty,
)
from tap_gitlab.api2._raw import (
    RawClient,
)
from tap_gitlab.api2._raw.page import (
    Page,
)
from tap_gitlab.api2._stream_utils import (
    GenericStream,
)
from tap_gitlab.api2._utils import (
    int_to_str,
)
from tap_gitlab.api2.job import (
    JobId,
    JobObj,
    JobStatus,
)
from tap_gitlab.api2.project import (
    ProjectId,
)
from typing import (
    Callable,
    Dict,
    FrozenSet,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class JobClient:
    _client: RawClient
    _proj: ProjectId

    def _raw_jobs_page(
        self, page: Page, scopes: FrozenSet[JobStatus]
    ) -> Cmd[FrozenList[JsonObj]]:
        params: Dict[str, JsonValue] = {
            "page": JsonValue(page.page_num),
            "per_page": JsonValue(page.per_page),
        }
        if scopes:
            params["scope[]"] = JsonValue(
                tuple(JsonValue(scope.value) for scope in scopes)
            )
        return self._client.get_list(
            "/projects/" + self._proj.to_str() + "/jobs", freeze(params)
        )

    def jobs_page(
        self, page: Page, scopes: FrozenSet[JobStatus]
    ) -> Cmd[FrozenList[JobObj]]:
        return self._raw_jobs_page(page, scopes).map(
            lambda js: tuple(decode_job_obj(j).unwrap() for j in js)
        )

    def job_stream(
        self, per_page: int, scopes: FrozenSet[JobStatus]
    ) -> Stream[JobObj]:
        return GenericStream(per_page).generic_page_stream(
            lambda p: self.jobs_page(p, scopes), GenericStream._is_empty
        )

    def jobs_ids_page(
        self, page: Page, scopes: FrozenSet[JobStatus]
    ) -> Cmd[FrozenList[JobId]]:
        return self._raw_jobs_page(page, scopes).map(
            lambda js: tuple(decode_job_id(j).unwrap() for j in js)
        )

    def job_id_stream(
        self, per_page: int, scopes: FrozenSet[JobStatus]
    ) -> Stream[JobId]:
        return GenericStream(per_page).generic_page_stream(
            lambda p: self.jobs_ids_page(p, scopes), GenericStream._is_empty
        )

    def cancel(self, job: JobId) -> Cmd[None]:
        proj_id: str = self._proj.to_str()
        job_id: str = int_to_str(job.job_id)
        return self._client.post(f"/projects/{proj_id}/jobs/{job_id}/cancel")
