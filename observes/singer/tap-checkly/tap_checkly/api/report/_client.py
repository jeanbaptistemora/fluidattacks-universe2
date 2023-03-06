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
    UnfoldedJVal,
)
from fa_purity.date_time import (
    DatetimeUTC,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
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
    DateRange,
    IndexedObj,
    ReportObj,
)
from typing import (
    Dict,
)


@dataclass(frozen=True)
class CheckReportClient:
    _client: RawClient

    def get_reports(
        self, from_date: DatetimeUTC, to_date: DatetimeUTC
    ) -> Cmd[FrozenList[CheckReport]]:
        args: Dict[str, UnfoldedJVal] = {
            "from": from_date.date_time.timestamp(),
            "to": to_date.date_time.timestamp(),
        }
        return self._client.get_list(
            "/v1/reporting",
            from_unfolded_dict(FrozenDict(args)),
        ).map(
            lambda l: pure_map(
                lambda i: CheckReportDecoder(i).decode_report().unwrap(), l
            ).to_list()
        )

    def get_reports_obj(
        self, from_date: DatetimeUTC, to_date: DatetimeUTC
    ) -> Cmd[FrozenList[ReportObj]]:
        _id = DateRange(from_date, to_date)
        return self.get_reports(from_date, to_date).map(
            lambda items: tuple(IndexedObj(_id, i) for i in items)
        )

    @staticmethod
    def new(
        auth: Credentials,
    ) -> CheckReportClient:
        return CheckReportClient(RawClient(auth))
