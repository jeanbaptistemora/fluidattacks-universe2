# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from jobs_scheduler.cron.core import (
    AnyTime,
    Cron,
    CronItem,
    DaysRange,
)


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


def match_cron(cron: Cron, time: datetime) -> bool:
    _week_day = (
        cron.week_day.to_cron()
        if isinstance(cron.week_day, DaysRange)
        else cron.week_day
    )
    return all(
        (
            match_cron_item(cron.minute, time.minute),
            match_cron_item(cron.hour, time.hour),
            match_cron_item(cron.day, time.day),
            match_cron_item(cron.month, time.month),
            match_cron_item(_week_day, _cron_weekday(time)),
        )
    )
