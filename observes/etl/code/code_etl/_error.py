import bugsnag
from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
    JsonValue,
    Result,
)
from typing import (
    Dict,
    NoReturn,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")
_F = TypeVar("_F")

# https://docs.bugsnag.com/platforms/python/other/#reporting-handled-errors
def notify_error(
    err: _T, metadata: Optional[FrozenDict[str, str]]
) -> Exception:
    exception = Exception(err)
    if metadata:
        _metadata: Dict[str, str] = dict(metadata)
        bugsnag.notify(exception, metadata=_metadata)
    else:
        bugsnag.notify(exception)
    exception.skip_bugsnag = True  # type: ignore[attr-defined]
    return exception


def group_metadata(group: str) -> FrozenDict[str, str]:
    return FrozenDict({"group": group})


def notify_and_raise(
    err: _T, metadata: Optional[FrozenDict[str, str]]
) -> NoReturn:
    raise notify_error(err, metadata)


def assert_or_raise(
    result: Result[_T, _F], metadata: Optional[FrozenDict[str, str]]
) -> _T:
    return result.alt(
        lambda e: notify_and_raise(e, metadata)  # type: ignore[misc]
    ).unwrap()
