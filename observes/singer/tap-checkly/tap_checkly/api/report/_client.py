# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from ._decode import (
    CheckReportDecoder,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    Stream,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from tap_checkly.api._raw import (
    Credentials,
    RawClient,
)
from tap_checkly.objs import (
    CheckReport,
)


@dataclass(frozen=True)
class CheckReportClient:
    _client: RawClient

    def get_reports(self) -> Cmd[FrozenList[CheckReport]]:
        return self._client.get_list("/v1/reporting", FrozenDict({}),).map(
            lambda l: pure_map(
                lambda i: CheckReportDecoder(i).decode_report().unwrap(), l
            ).to_list()
        )

    def reports_stream(self) -> Stream[CheckReport]:
        return unsafe_from_cmd(self.get_reports().map(from_flist))

    @staticmethod
    def new(
        auth: Credentials,
    ) -> CheckReportClient:
        return CheckReportClient(RawClient(auth))
