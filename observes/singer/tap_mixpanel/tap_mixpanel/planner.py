# Standard libraries
import datetime
from typing import (
    NamedTuple,
    Optional,
    Union,
)

# Third party libraries
import pandas

# Local libraries


Date = datetime.date
Interval = Union[pandas.Interval]
IntervalIndex = Union[pandas.IntervalIndex]


class TargetDates(NamedTuple):
    previous_ranges: IntervalIndex
    actual_range: Optional[Interval]


def previous_date_ranges(init_date: Date) -> IntervalIndex:
    offset = pandas.offsets.MonthBegin(n=1)
    date_range = pandas.interval_range(
        start=init_date - offset,
        end=datetime.date.today(),
        freq='MS',
        closed='left'
    )
    return date_range


def target_dates(init_date: Date) -> TargetDates:
    offset = pandas.offsets.MonthBegin(n=1)
    today = datetime.date.today()
    previous_ranges = previous_date_ranges(init_date)
    actual_range = Interval(left=today - offset, right=today, closed='both')
    return TargetDates(
        previous_ranges=previous_ranges,
        actual_range=None
        if any(previous_ranges.contains(today))
        else actual_range
    )
