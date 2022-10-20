# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from ._decode import (
    CheckDecoder,
)
from .results import (
    CheckResultClient,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Stream,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.pure_iter.factory import (
    pure_map,
)
from tap_checkly.api import (
    _utils,
)
from tap_checkly.api._raw import (
    Credentials,
    RawClient,
)
from tap_checkly.objs import (
    CheckId,
    CheckObj,
    CheckResultObj,
)


@dataclass(frozen=True)
class ChecksClient:
    _raw: RawClient
    _per_page: int
    _from_date: datetime
    _to_date: datetime

    def _list_ids(self, page: int) -> Cmd[FrozenList[CheckId]]:
        return self._raw.get_list(
            "/v1/checks",
            from_prim_dict({"limit": self._per_page, "page": page}),
        ).map(
            lambda l: pure_map(
                lambda i: CheckDecoder(i).decode_id().unwrap(), l
            ).to_list()
        )

    def list_ids(self) -> Stream[CheckId]:
        return _utils.paginate_all(self._list_ids)

    def _list_checks(self, page: int) -> Cmd[FrozenList[CheckObj]]:
        return self._raw.get_list(
            "/v1/checks",
            from_prim_dict({"limit": self._per_page, "page": page}),
        ).map(
            lambda l: pure_map(
                lambda i: CheckDecoder(i).decode_obj().unwrap(), l
            ).to_list()
        )

    def list_checks(self) -> Stream[CheckObj]:
        return _utils.paginate_all(self._list_checks)

    def list_check_results(self, check: CheckId) -> Stream[CheckResultObj]:
        _client = CheckResultClient(
            self._raw, check, self._per_page, self._from_date, self._to_date
        )
        return _client.list_all()

    @staticmethod
    def new(
        auth: Credentials,
        per_page: int,
        from_date: datetime,
        to_date: datetime,
    ) -> ChecksClient:
        return ChecksClient(RawClient(auth), per_page, from_date, to_date)
