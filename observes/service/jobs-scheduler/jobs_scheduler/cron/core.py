# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    ResultE,
)
from fa_purity.result import (
    Result,
)
from typing import (
    Callable,
    FrozenSet,
    Optional,
    TypeVar,
    Union,
)

_R = TypeVar("_R")


@dataclass(frozen=True)
class _CronItem:
    values: Optional[FrozenSet[int]]
    value_range: Optional[range]
    any: bool


@dataclass(frozen=True)
class CronItem:
    _inner: _CronItem

    @staticmethod
    def from_values(raw: Union[int, FrozenSet[int]]) -> CronItem:
        values = raw if isinstance(raw, frozenset) else frozenset([raw])
        return CronItem(_CronItem(values, None, False))

    @staticmethod
    def from_range(raw: range) -> CronItem:
        return CronItem(_CronItem(None, raw, False))

    @staticmethod
    def any() -> CronItem:
        return CronItem(_CronItem(None, None, True))

    def transform(
        self,
        value_handler: Callable[[FrozenSet[int]], _R],
        range_handler: Callable[[range], _R],
        any_handler: _R,
    ) -> _R:
        if self._inner.any:
            return any_handler
        if self._inner.values:
            return value_handler(self._inner.values)
        if self._inner.value_range:
            return range_handler(self._inner.value_range)
        raise Exception("Bad builded CronItem")


class Days(Enum):
    SUN = 0
    MON = 1
    TUE = 2
    WEN = 3
    THU = 4
    FRI = 5
    SAT = 6


@dataclass(frozen=True)
class _DaysRange:
    from_day: Days
    to_day: Days


@dataclass(frozen=True)
class DaysRange:
    _inner: _DaysRange

    @staticmethod
    def new(_from: Days, _to: Days) -> ResultE[DaysRange]:
        if _from != _to:
            return Result.success(DaysRange(_DaysRange(_from, _to)))
        return Result.failure(
            Exception("DaysRange _from and _to must be different")
        )

    def to_cron(self) -> CronItem:
        if self._inner.from_day.value < self._inner.to_day.value:
            return CronItem.from_range(
                range(self._inner.from_day.value, self._inner.to_day.value + 1)
            )
        return CronItem.from_values(
            frozenset(
                range(self._inner.from_day.value, Days.SAT.value + 1)
            ).union(range(0, self._inner.to_day.value + 1))
        )


@dataclass(frozen=True)
class CronDraft:
    minute: CronItem
    hour: CronItem
    day: CronItem
    month: CronItem
    week_day: Union[CronItem, DaysRange]


@dataclass(frozen=True)
class _Cron:
    cron: CronDraft


@dataclass(frozen=True)
class Cron:
    _inner: _Cron
    minute: CronItem
    hour: CronItem
    day: CronItem
    month: CronItem
    week_day: Union[CronItem, DaysRange]

    @staticmethod
    def _valid_cron(item: CronItem, constraint: range) -> bool:
        return item.transform(
            lambda items: all(i in constraint for i in items),
            lambda _range: _range.start >= constraint.start
            and _range.stop <= constraint.stop,
            True,
        )

    @classmethod
    def new_cron(cls, draft: CronDraft) -> ResultE[Cron]:
        _week_day = (
            draft.week_day.to_cron()
            if isinstance(draft.week_day, DaysRange)
            else draft.week_day
        )
        if all(
            (
                cls._valid_cron(draft.minute, range(0, 60)),
                cls._valid_cron(draft.hour, range(0, 24)),
                cls._valid_cron(draft.day, range(1, 32)),
                cls._valid_cron(draft.month, range(1, 13)),
                cls._valid_cron(_week_day, range(0, 7)),
            )
        ):
            return Result.success(
                Cron(
                    _Cron(draft),
                    draft.minute,
                    draft.hour,
                    draft.day,
                    draft.month,
                    draft.week_day,
                )
            )
        return Result.failure(ValueError("Invalid Cron"), Cron).alt(Exception)
