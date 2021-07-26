from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
import pytz
from returns.io import (
    IO,
)


@dataclass(frozen=True)
class DateTime:
    _date: datetime


def now() -> IO[DateTime]:
    return IO(DateTime(datetime.now(pytz.utc)))
