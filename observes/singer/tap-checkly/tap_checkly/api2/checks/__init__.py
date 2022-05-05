from __future__ import (
    annotations,
)

from .results import (
    CheckResultClient,
    CheckResultObj,
)
from .results.time_range import (
    date_ranges_dsc,
    DateRange,
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
    JsonObj,
    Maybe,
    PureIter,
    Stream,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.json.value.transform import (
    Unfolder,
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
    until_none,
)
from tap_checkly.api2._raw import (
    Credentials,
    RawClient,
)
from tap_checkly.api2.checks.core import (
    CheckId,
)


def _check_id_from_raw(raw: JsonObj) -> CheckId:
    _id = Unfolder(raw["id"]).to_primitive(str).unwrap()
    return CheckId(_id)


@dataclass(frozen=True)
class ChecksClient:
    _raw: RawClient
    _per_page: int
    _from_date: datetime
    _to_date: datetime

    def list_checks(self, page: int) -> Cmd[FrozenList[CheckId]]:
        return self._raw.get_list(
            "/v1/checks",
            from_prim_dict({"limit": self._per_page, "page": page}),
        ).map(lambda l: tuple(map(_check_id_from_raw, l)))

    def date_ranges(self) -> PureIter[DateRange]:
        return date_ranges_dsc(self._from_date, self._to_date)

    def _list_check_results(
        self, check: CheckId, dr: DateRange
    ) -> Cmd[Maybe[Stream[CheckResultObj]]]:
        _results = CheckResultClient(self._raw, check)
        first = _results.list_check_results(1, self._per_page, dr)
        return first.map(
            lambda i: Maybe.from_optional(i if bool(i) else None).map(
                lambda f: infinite_range(1, 1)
                .map(
                    lambda p: _results.list_check_results(
                        p, self._per_page, dr
                    )
                    if p > 1
                    else Cmd.from_cmd(lambda: f)
                )
                .transform(lambda x: from_piter(x))
                .map(lambda i: i if bool(i) else None)
                .transform(lambda x: until_none(x))
                .map(lambda x: from_flist(x))
                .transform(lambda x: chain(x))
            )
        )

    def list_check_results(self, chk_id: CheckId) -> Stream[CheckResultObj]:
        return (
            self.date_ranges()
            .map(lambda dr: self._list_check_results(chk_id, dr))
            .transform(lambda x: from_piter(x))
            .transform(lambda x: until_empty(x))
            .bind(lambda s: s)
        )

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
