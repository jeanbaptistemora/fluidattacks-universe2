from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
    timezone,
)


@dataclass(frozen=True)
class _DatetimeUTC:
    time: datetime


@dataclass(frozen=True)
class DatetimeUTC(_DatetimeUTC):
    def __init__(self, obj: _DatetimeUTC) -> None:
        super().__init__(obj.time)


def to_utc(time: datetime) -> DatetimeUTC:
    draft = _DatetimeUTC(time.astimezone(timezone.utc))
    return DatetimeUTC(draft)
