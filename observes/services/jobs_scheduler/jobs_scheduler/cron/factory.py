from fa_purity.result import (
    Result,
)
from jobs_scheduler.cron.core import (
    _Cron,
    AnyTime,
    Cron,
    CronDraft,
    CronItem,
    InvalidCron,
)


def _valid_cron(item: CronItem, constraint: range) -> bool:
    if isinstance(item, AnyTime):
        return True
    if isinstance(item, range):
        return item.start >= constraint.start and item.stop <= constraint.stop
    if isinstance(item, tuple):
        return all(i in constraint for i in item)
    elem: int = item
    return elem in constraint


def new(draft: CronDraft) -> Result[Cron, InvalidCron]:
    if all(
        (
            _valid_cron(draft.minute, range(0, 60)),
            _valid_cron(draft.hour, range(0, 24)),
            _valid_cron(draft.day, range(1, 32)),
            _valid_cron(draft.month, range(1, 13)),
            _valid_cron(draft.week_day, range(0, 7)),
        )
    ):
        return Result.success(Cron(_Cron(draft)))
    return Result.failure(InvalidCron())


def weekly(
    minute: CronItem, hour: CronItem, week_day: CronItem
) -> Result[Cron, InvalidCron]:
    return new(CronDraft(minute, hour, AnyTime(), AnyTime(), week_day))


def work_days(minute: CronItem, hour: CronItem) -> Result[Cron, InvalidCron]:
    days = range(1, 6)  # Monday - Friday
    return new(CronDraft(minute, hour, AnyTime(), AnyTime(), days))


def week_days(
    minute: CronItem, hour: CronItem, days: CronItem
) -> Result[Cron, InvalidCron]:
    return new(CronDraft(minute, hour, AnyTime(), AnyTime(), days))
