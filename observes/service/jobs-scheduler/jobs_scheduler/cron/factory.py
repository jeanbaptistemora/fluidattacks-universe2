# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity.result import (
    Result,
)
from jobs_scheduler.cron.core import (
    AnyTime,
    Cron,
    CronDraft,
    CronItem,
    Days,
    DaysRange,
    InvalidCron,
    new_cron,
)
from typing import (
    Union,
)


def weekly(
    minute: CronItem, hour: CronItem, week_day: CronItem
) -> Result[Cron, InvalidCron]:
    return new_cron(CronDraft(minute, hour, AnyTime(), AnyTime(), week_day))


def work_days(minute: CronItem, hour: CronItem) -> Result[Cron, InvalidCron]:
    days = DaysRange(Days.MON, Days.FRI)
    return new_cron(CronDraft(minute, hour, AnyTime(), AnyTime(), days))


def week_days(
    minute: CronItem, hour: CronItem, days: Union[CronItem, DaysRange]
) -> Result[Cron, InvalidCron]:
    return new_cron(CronDraft(minute, hour, AnyTime(), AnyTime(), days))


__all__ = [
    "new_cron",
]
