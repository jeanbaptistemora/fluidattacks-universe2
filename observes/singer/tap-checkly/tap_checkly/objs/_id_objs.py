from dataclasses import (
    dataclass,
)
from fa_purity.date_time import (
    DatetimeUTC,
)
from typing import (
    Generic,
    TypeVar,
)

_ID = TypeVar("_ID")
_T = TypeVar("_T")


@dataclass(frozen=True)
class IndexedObj(Generic[_ID, _T]):
    id_obj: _ID
    obj: _T


@dataclass(frozen=True)
class DateRange:
    from_date: DatetimeUTC
    to_date: DatetimeUTC
