from datetime import (
    timedelta,
)
from fa_purity import (
    FrozenList,
    PureIter,
    Stream,
)
from fa_purity.date_time import (
    DatetimeUTC,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
)
import math
from tap_checkly.api.report import (
    CheckReportClient,
)
from tap_checkly.objs import (
    ReportObj,
)


def _date_range_per_day(
    start: DatetimeUTC, end: DatetimeUTC
) -> PureIter[DatetimeUTC]:
    days = math.ceil((end.date_time - start.date_time) / timedelta(days=1))
    return from_range(range(0, days)).map(lambda d: start + timedelta(days=d))


def daily_reports(
    client: CheckReportClient, from_date: DatetimeUTC, to_date: DatetimeUTC
) -> Stream[ReportObj]:
    items = (
        _date_range_per_day(from_date, to_date)
        .map(lambda d: client.get_reports_obj(d, d + timedelta(days=1)))
        .transform(lambda x: from_piter(x))
    )
    return items.map(lambda x: from_flist(x)).transform(lambda s: chain(s))
