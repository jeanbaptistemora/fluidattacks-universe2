from datetime import (
    datetime,
)
from dateutil.parser import (
    isoparse,
)
from fa_purity import (
    Result,
    ResultE,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


def handle_value_error(function: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(function())
    except ValueError as err:
        return Result.failure(err)


def to_datetime(raw: str) -> ResultE[datetime]:
    return handle_value_error(lambda: isoparse(raw))
