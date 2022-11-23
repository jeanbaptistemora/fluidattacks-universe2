from fa_purity.result import (
    ResultE,
)
from jobs_scheduler.cron.core import (
    Cron,
    CronDraft,
    CronItem,
    Days,
    DaysRange,
)
from typing import (
    FrozenSet,
    Union,
)


def _to_cron(item: CronItem | int) -> CronItem:
    if isinstance(item, CronItem):
        return item
    return CronItem.from_values(item)


def weekly(
    minute: CronItem | int,
    hour: CronItem | int,
    week_days: Union[FrozenSet[Days], DaysRange],
) -> ResultE[Cron]:
    _week_days: DaysRange | CronItem = (
        week_days
        if isinstance(week_days, DaysRange)
        else CronItem.from_values(frozenset(w.value for w in week_days))
    )
    return Cron.new_cron(
        CronDraft(
            _to_cron(minute),
            _to_cron(hour),
            CronItem.any(),
            CronItem.any(),
            _week_days,
        )
    )


def work_days(minute: CronItem | int, hour: CronItem | int) -> ResultE[Cron]:
    days = DaysRange.new(Days.MON, Days.FRI)
    return days.bind(
        lambda d: Cron.new_cron(
            CronDraft(
                _to_cron(minute),
                _to_cron(hour),
                CronItem.any(),
                CronItem.any(),
                d,
            )
        )
    )


def behind_work_days(minute: CronItem | int, hour: CronItem | int) -> Cron:
    return weekly(
        _to_cron(minute),
        _to_cron(hour),
        DaysRange.new(Days.SUN, Days.THU).unwrap(),
    ).unwrap()
