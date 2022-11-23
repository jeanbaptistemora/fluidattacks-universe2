from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
    timedelta,
)
from fa_purity import (
    PureIter,
    Result,
    ResultE,
)
from fa_purity.pure_iter import (
    transform as piter_transform,
)
from fa_purity.pure_iter.factory import (
    infinite_range,
)


class OutOfRange(Exception):
    pass


@dataclass(frozen=True)
class _DateRange:
    from_date: datetime
    to_date: datetime


@dataclass(frozen=True)
class DateRange(_DateRange):
    def __init__(self, obj: _DateRange) -> None:
        super().__init__(**obj.__dict__)  # type: ignore [misc]

    @staticmethod
    def new(from_date: datetime, to_date: datetime) -> ResultE[DateRange]:
        delta = to_date - from_date
        if delta <= timedelta(hours=6):
            item = DateRange(_DateRange(from_date, to_date))
            return Result.success(item)
        return Result.failure(
            OutOfRange("time delta of DateRange must be <= 6h"),
            DateRange,
        ).alt(Exception)


def _lower_limit(date: datetime, limit: datetime) -> datetime:
    return limit if date < limit else date


def date_ranges_dsc(
    from_date: datetime, to_date: datetime
) -> PureIter[DateRange]:
    return (
        infinite_range(0, 6)
        .map(
            lambda h: DateRange.new(
                _lower_limit(to_date - timedelta(hours=h + 6), from_date),
                to_date - timedelta(hours=h),
            ).unwrap()
        )
        .map(lambda dr: None if dr.to_date <= from_date else dr)
        .transform(lambda x: piter_transform.until_none(x))
    )
