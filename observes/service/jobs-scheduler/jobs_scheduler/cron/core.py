from dataclasses import (
    dataclass,
)
from fa_purity.result import (
    Result,
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


@dataclass(frozen=True)
class CronDraft:
    minute: CronItem
    hour: CronItem
    day: CronItem
    month: CronItem
    week_day: CronItem


@dataclass(frozen=True)
class _Cron:
    inner: CronDraft


@dataclass(frozen=True)
class Cron(CronDraft):
    def __init__(self, obj: _Cron) -> None:
        super().__init__(**obj.inner.__dict__)  # type: ignore[misc]


def _valid_cron(item: CronItem, constraint: range) -> bool:
    if isinstance(item, AnyTime):
        return True
    if isinstance(item, range):
        return item.start >= constraint.start and item.stop <= constraint.stop
    if isinstance(item, tuple):
        return all(i in constraint for i in item)
    elem: int = item
    return elem in constraint


def new_cron(draft: CronDraft) -> Result[Cron, InvalidCron]:
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
