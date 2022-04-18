from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from pyrfc3339 import (  # type: ignore
    generate,
    parse as parse_rfc3339,
)
import pytz  # type: ignore
from returns.io import (
    IO,
)


@dataclass(frozen=True)
class _DateTime:
    date: datetime


@dataclass(frozen=True)
class DateTime(_DateTime):
    def __init__(self, obj: _DateTime) -> None:
        super().__init__(obj.date)

    def to_utc_str(self) -> str:
        return generate(self.date)

    def to_str(self) -> str:
        return generate(self.date, utc=False)


@dataclass(frozen=True)
class TimeFactory:
    @classmethod
    def now(cls) -> IO[DateTime]:
        draft = _DateTime(datetime.now(pytz.utc))
        return IO(DateTime(draft))

    @classmethod
    def parse(cls, raw: str) -> DateTime:
        draft = _DateTime(parse_rfc3339(raw))
        return DateTime(draft)
