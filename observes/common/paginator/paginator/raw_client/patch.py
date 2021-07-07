from dataclasses import (
    dataclass,
)
from typing import (
    Generic,
    TypeVar,
)

_Point = TypeVar("_Point")


@dataclass(frozen=True)
class Patch(Generic[_Point]):
    # patch for https://github.com/python/mypy/issues/5485
    # upgrading mypy where the fix is included will deprecate this
    inner: _Point

    @property
    def unwrap(self) -> _Point:
        return self.inner
