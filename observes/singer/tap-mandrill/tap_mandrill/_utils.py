from datetime import (
    datetime,
)
from dateutil import (
    parser,
)
from fa_purity import (
    FrozenDict,
    Maybe,
    Result,
    ResultE,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


def handle_value_error(non_total_function: Callable[[], _T]) -> ResultE[_T]:
    try:
        return Result.success(non_total_function())
    except ValueError as err:
        return Result.failure(err)


def isoparse(raw: str) -> ResultE[datetime]:
    return handle_value_error(lambda: parser.isoparse(raw))


def to_int(raw: str) -> ResultE[int]:
    return handle_value_error(lambda: int(raw))


def get_item(raw: FrozenDict[str, _T], key: str) -> ResultE[_T]:
    return (
        Maybe.from_optional(raw.get(key))
        .to_result()
        .alt(lambda _: KeyError(key))
    )
