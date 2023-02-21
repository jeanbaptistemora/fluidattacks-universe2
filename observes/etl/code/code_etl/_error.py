import bugsnag
from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenList,
    JsonValue,
    Result,
)
from typing import (
    Dict,
    NoReturn,
    TypeVar,
)

_S = TypeVar("_S")


@dataclass(frozen=True)
class NotifiedException(Exception):
    err: Exception
    skip_bugsnag: bool


def notify_error(group: str, err: Exception) -> Exception:
    metadata: Dict[str, str] = {"group": group}
    bugsnag.notify(err, metadata=metadata)
    return NotifiedException(err, True)


def notify_and_raise(group: str, err: Exception) -> NoReturn:
    metadata: Dict[str, str] = {"group": group}
    bugsnag.notify(err, metadata=metadata)
    raise NotifiedException(err, True)


def assert_or_raise(group: str, result: Result[_S, Exception]) -> _S:
    return result.alt(
        lambda e: notify_and_raise(group, e)  # type: ignore[misc]
    ).unwrap()
