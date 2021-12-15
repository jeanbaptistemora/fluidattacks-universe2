from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from jobs_scheduler.cron_2.core import (
    AnyTime,
    CronItem,
    InvalidCron,
)
from typing import (
    NamedTuple,
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


class PartialCron(NamedTuple):
    hour: CronItem
    day: CronItem
    week_day: CronItem

    @classmethod
    def new(
        cls, hour: CronItem, day: CronItem, week_day: CronItem
    ) -> PartialCron:
        if all(
            (
                _valid_cron(hour, range(0, 24)),
                _valid_cron(day, range(1, 32)),
                _valid_cron(week_day, range(0, 7)),
            )
        ):
            return cls(hour, day, week_day)
        raise InvalidCron()


def match_cron_item(item: CronItem, value: int) -> bool:
    if isinstance(item, AnyTime):
        return True
    if isinstance(item, (range, tuple)):
        return value in item
    elem: int = item
    return elem == value


def _cron_weekday(time: datetime) -> int:
    wday = time.weekday() + 1
    return wday if wday < 7 else 0


def match_cron(cron: PartialCron, time: datetime) -> bool:
    return all(
        (
            match_cron_item(cron.hour, time.hour),
            match_cron_item(cron.day, time.day),
            match_cron_item(cron.week_day, _cron_weekday(time)),
        )
    )


__all__ = [
    "AnyTime",
]
