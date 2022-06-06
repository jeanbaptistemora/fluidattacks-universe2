from __future__ import (
    annotations,
)

from . import (
    _decode,
)
from ._core import (
    CheckId,
    CheckObj,
)
from .results import (
    CheckResultClient,
    CheckResultObj,
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
from tap_checkly.api2 import (
    _utils,
)
from tap_checkly.api2._raw import (
    Credentials,
    RawClient,
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
        ).map(lambda l: tuple(map(_decode.id_from_raw, l)))

    def list_ids(self) -> Stream[CheckId]:
        return _utils.paginate_all(self._list_ids)

    def _list_checks(self, page: int) -> Cmd[FrozenList[CheckObj]]:
        return self._raw.get_list(
            "/v1/checks",
            from_prim_dict({"limit": self._per_page, "page": page}),
        ).map(lambda l: tuple(map(_decode.from_raw_obj, l)))

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


__all__ = [
    "CheckId",
]
