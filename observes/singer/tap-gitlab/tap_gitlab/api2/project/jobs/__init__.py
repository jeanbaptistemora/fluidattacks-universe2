# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0
from __future__ import (
    annotations,
)

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
    Stream,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from tap_gitlab.api2._raw import (
    Credentials,
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
    Dict,
    FrozenSet,
)

LOG = logging.getLogger(__name__)


def raise_and_log(err: Exception, at_input: str) -> None:
    LOG.error("Error at input %s", at_input)
    raise_exception(err)


@dataclass(frozen=True)
class JobClient:
    _client: RawClient
    _proj: ProjectId

    @staticmethod
    def new(creds: Credentials, proj: ProjectId) -> JobClient:
        raw = RawClient.new(creds)
        return JobClient(raw, proj)

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
            lambda js: tuple(
                decode_job_obj(j)
                .alt(lambda e: raise_and_log(e, str(j)))
                .unwrap()
                for j in js
            )
        )

    def job_stream(
        self, start_page: int, per_page: int, scopes: FrozenSet[JobStatus]
    ) -> Stream[JobObj]:
        return GenericStream(start_page, per_page).generic_page_stream(
            lambda p: self.jobs_page(p, scopes), GenericStream._is_empty
        )

    def jobs_ids_page(
        self, page: Page, scopes: FrozenSet[JobStatus]
    ) -> Cmd[FrozenList[JobId]]:
        return self._raw_jobs_page(page, scopes).map(
            lambda js: tuple(decode_job_id(j).unwrap() for j in js)
        )

    def job_id_stream(
        self, start_page: int, per_page: int, scopes: FrozenSet[JobStatus]
    ) -> Stream[JobId]:
        return GenericStream(start_page, per_page).generic_page_stream(
            lambda p: self.jobs_ids_page(p, scopes), GenericStream._is_empty
        )

    def cancel(self, job: JobId) -> Cmd[None]:
        proj_id: str = self._proj.to_str()
        job_id: str = int_to_str(job.job_id)
        return self._client.post(f"/projects/{proj_id}/jobs/{job_id}/cancel")
