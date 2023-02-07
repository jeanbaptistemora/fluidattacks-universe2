from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)
from fa_purity import (
    ResultE,
)
from fa_purity.result import (
    Result,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class DatetimeTZ:
    _private: _Private = field(repr=False, hash=False, compare=False)
    time: datetime

    @staticmethod
    def assert_tz(time: datetime) -> ResultE[DatetimeTZ]:
        if time.tzinfo is not None:
            return Result.success(DatetimeTZ(_Private(), time))
        err = ValueError("datetime must have a timezone")
        return Result.failure(err, DatetimeTZ).alt(Exception)

    def to_tz(self, time_zone: timezone) -> DatetimeTZ:
        return self.assert_tz(self.time.astimezone(time_zone)).unwrap()


@dataclass(frozen=True)
class DatetimeUTC:
    _private: _Private = field(repr=False, hash=False, compare=False)
    time: datetime

    @staticmethod
    def assert_utc(time: datetime | DatetimeTZ) -> ResultE[DatetimeUTC]:
        _time = time if isinstance(time, datetime) else time.time
        if _time.tzinfo == timezone.utc:
            return Result.success(DatetimeUTC(_Private(), _time))
        err = ValueError(
            f"datetime must have UTC timezone but got {_time.tzinfo}"
        )
        return Result.failure(err, DatetimeUTC).alt(Exception)

    @classmethod
    def to_utc(cls, time: DatetimeTZ) -> DatetimeUTC:
        return cls.assert_utc(time.to_tz(timezone.utc)).unwrap()


DATE_NOW: DatetimeUTC = DatetimeUTC.assert_utc(
    datetime.now(timezone.utc)
).unwrap()
EPOCH_START: DatetimeUTC = DatetimeUTC.assert_utc(
    datetime.fromtimestamp(0, timezone.utc)
).unwrap()
