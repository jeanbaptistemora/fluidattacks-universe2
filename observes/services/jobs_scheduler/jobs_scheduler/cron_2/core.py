from dataclasses import (
    dataclass,
)
from typing import (
    Tuple,
    Union,
)


class InvalidCron(Exception):
    pass


@dataclass(frozen=True)
class AnyTime:
    pass


CronItem = Union[int, Tuple[int, ...], range, AnyTime]
work_days = range(1, 6)  # Monday - Friday


@dataclass(frozen=True)
class CronDraft:
    minute: CronItem
    hour: CronItem
    day: CronItem
    month: CronItem
    week_day: CronItem


@dataclass(frozen=True)
class _Cron(CronDraft):
    def __init__(self, obj: CronDraft) -> None:
        super().__init__(**obj.__dict__)


@dataclass(frozen=True)
class Cron(_Cron):
    def __init__(self, obj: _Cron) -> None:
        super().__init__(**obj.__dict__)
