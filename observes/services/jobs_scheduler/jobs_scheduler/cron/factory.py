from fa_purity.result import (
    Result,
)
from jobs_scheduler.cron.core import (
    AnyTime,
    Cron,
    CronDraft,
    CronItem,
    InvalidCron,
    new_cron,
)


def weekly(
    minute: CronItem, hour: CronItem, week_day: CronItem
) -> Result[Cron, InvalidCron]:
    return new_cron(CronDraft(minute, hour, AnyTime(), AnyTime(), week_day))


def work_days(minute: CronItem, hour: CronItem) -> Result[Cron, InvalidCron]:
    days = range(1, 6)  # Monday - Friday
    return new_cron(CronDraft(minute, hour, AnyTime(), AnyTime(), days))


def week_days(
    minute: CronItem, hour: CronItem, days: CronItem
) -> Result[Cron, InvalidCron]:
    return new_cron(CronDraft(minute, hour, AnyTime(), AnyTime(), days))


__all__ = [
    "new_cron",
]
